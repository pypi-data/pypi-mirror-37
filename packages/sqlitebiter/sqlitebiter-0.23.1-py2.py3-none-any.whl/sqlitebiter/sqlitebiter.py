#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import errno
import os
import sys
from textwrap import dedent

import click
import logbook
import logbook.more
import path
import pytablereader as ptr
import simplesqlite as sqlite
import typepy

from .__version__ import __version__
from ._common import DEFAULT_DUP_COL_HANDLER
from ._config import ConfigKey, app_config_manager
from ._const import IPYNB_FORMAT_NAME_LIST, PROGRAM_NAME
from ._enum import Context, DupDatabase, ExitCode
from .subcommand import FileConverter, GoogleSheetsConverter, UrlConverter


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], obj={})
QUIET_LOG_LEVEL = logbook.NOTSET
COMMAND_EPILOG = dedent(
    """\
    Documentation: https://sqlitebiter.rtfd.io/
    Issue tracker: https://github.com/thombashi/sqlitebiter/issues
    """
)

logbook.more.ColorizedStderrHandler(
    level=logbook.DEBUG, format_string="[{record.level_name}] {record.channel}: {record.message}"
).push_application()


class Default(object):
    OUTPUT_FILE = "out.sqlite"
    ENCODING = "utf-8"


def create_database(database_path, dup_table):
    db_path = path.Path(database_path)
    dir_path = db_path.dirname()

    if typepy.is_not_null_string(dir_path):
        dir_path.makedirs_p()

    is_create_db = not db_path.isfile()

    if dup_table == DupDatabase.APPEND:
        return (sqlite.SimpleSQLite(db_path, "a"), is_create_db)

    return (sqlite.SimpleSQLite(db_path, "w"), is_create_db)


def make_logger(channel_name, log_level):
    import appconfigpy

    logger = logbook.Logger(channel_name)

    if log_level == QUIET_LOG_LEVEL:
        logger.disable()

    logger.level = log_level
    ptr.set_log_level(log_level)
    sqlite.set_log_level(log_level)
    appconfigpy.set_log_level(log_level)

    return logger


def finalize(con, converter, is_create_db):
    converter.write_completion_message()
    database_path = con.database_path
    con.close()

    if all([os.path.isfile(database_path), converter.get_success_count() == 0, is_create_db]):
        os.remove(database_path)

    return converter.get_return_code()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__, message="%(prog)s %(version)s")
@click.option(
    "-o",
    "--output-path",
    metavar="PATH",
    default=Default.OUTPUT_FILE,
    help="Output path of the SQLite database file. Defaults to '{:s}'.".format(Default.OUTPUT_FILE),
)
@click.option(
    "-a", "--append", "is_append_table", is_flag=True, help="append table(s) to existing database."
)
@click.option(
    "-i",
    "--index",
    "index_list",
    default="",
    help="comma separated attribute names to create indices.",
)
@click.option("--replace-symbol", "symbol_replace_value", help="Replace symbols in attributes.")
@click.option("-v", "--verbose", "verbosity_level", count=True)
@click.option("--debug", "log_level", flag_value=logbook.DEBUG, help="for debug print.")
@click.option(
    "-q",
    "--quiet",
    "log_level",
    flag_value=QUIET_LOG_LEVEL,
    help="suppress execution log messages.",
)
@click.pass_context
def cmd(
    ctx, output_path, is_append_table, index_list, symbol_replace_value, verbosity_level, log_level
):
    ctx.obj[Context.OUTPUT_PATH] = output_path
    ctx.obj[Context.SYMBOL_REPLACE_VALUE] = symbol_replace_value
    ctx.obj[Context.DUP_DATABASE] = DupDatabase.APPEND if is_append_table else DupDatabase.OVERWRITE
    ctx.obj[Context.INDEX_LIST] = index_list.split(",")
    ctx.obj[Context.VERBOSITY_LEVEL] = verbosity_level
    ctx.obj[Context.LOG_LEVEL] = logbook.INFO if log_level is None else log_level

    sqlite.SimpleSQLite.dup_col_handler = DEFAULT_DUP_COL_HANDLER


@cmd.command(epilog=COMMAND_EPILOG)
@click.argument("files", type=str, nargs=-1)
@click.option(
    "-r", "--recursive", is_flag=True, help="Read all files under each directory, recursively."
)
@click.option("--pattern", metavar="PATTERN", help="Convert files matching PATTERN.")
@click.option("--exclude", metavar="PATTERN", help="Exclude files matching PATTERN.")
@click.option("--follow-symlinks", is_flag=True, help="Follow symlinks.")
@click.option(
    "-f",
    "--format",
    "format_name",
    type=click.Choice(ptr.TableFileLoader.get_format_name_list() + IPYNB_FORMAT_NAME_LIST),
    help="Data format to loading (auto-detect from file extensions in default).",
)
@click.option(
    "--encoding",
    metavar="ENCODING",
    help="Encoding to load files. Auto-detection from files in default.",
)
@click.pass_context
def file(ctx, files, recursive, pattern, exclude, follow_symlinks, format_name, encoding):
    """
    Convert tabular data within
    CSV/Excel/HTML/JSON/Jupyter Notebook/LDJSON/LTSV/Markdown/Mediawiki/SQLite/SSV/TSV
    file(s) or named pipes to a SQLite database file.
    """

    logger = make_logger("{:s} file".format(PROGRAM_NAME), ctx.obj[Context.LOG_LEVEL])

    if typepy.is_empty_sequence(files):
        logger.error("require at least one file specification.\n\n{}".format(ctx.get_help()))
        sys.exit(ExitCode.NO_INPUT)

    con, is_create_db = create_database(ctx.obj[Context.OUTPUT_PATH], ctx.obj[Context.DUP_DATABASE])
    converter = FileConverter(
        logger=logger,
        con=con,
        symbol_replace_value=ctx.obj[Context.SYMBOL_REPLACE_VALUE],
        index_list=ctx.obj.get(Context.INDEX_LIST),
        verbosity_level=ctx.obj.get(Context.VERBOSITY_LEVEL),
        format_name=format_name,
        encoding=encoding,
        exclude_pattern=exclude,
        follow_symlinks=follow_symlinks,
    )

    for file_path in files:
        dir_path_obj = path.Path(file_path)

        if not follow_symlinks and dir_path_obj.islink() and dir_path_obj.isdir():
            logger.debug(
                "skip symlink to a directory: {} -> {}".format(
                    dir_path_obj, dir_path_obj.readlink()
                )
            )
            continue

        if recursive and dir_path_obj.isdir():
            for file_path_obj in dir_path_obj.walkfiles(pattern):
                converter.convert(file_path_obj)
        else:
            converter.convert(file_path)

    sys.exit(finalize(con, converter, is_create_db))


@cmd.command(epilog=COMMAND_EPILOG)
@click.argument("url", type=str)
@click.option(
    "-f",
    "--format",
    "format_name",
    type=click.Choice(ptr.TableUrlLoader.get_format_name_list() + IPYNB_FORMAT_NAME_LIST),
    help="Data format to loading (defaults to html).",
)
@click.option(
    "-e",
    "--encoding",
    type=str,
    metavar="ENCODING",
    help="HTML page read encoding. Defaults to {:s}.".format(Default.ENCODING),
)
@click.option(
    "-p",
    "--proxy",
    type=str,
    metavar="PROXY",
    help="Specify a proxy in the form [user:passwd@]proxy.server:port.",
)
@click.pass_context
def url(ctx, url, format_name, encoding, proxy):
    """
    Scrape tabular data from a URL and convert data to a SQLite database file.
    """

    if typepy.is_empty_sequence(url):
        sys.exit(ExitCode.NO_INPUT)

    logger = make_logger("{:s} url".format(PROGRAM_NAME), ctx.obj[Context.LOG_LEVEL])

    if typepy.is_empty_sequence(encoding):
        encoding = app_config_manager.load().get(ConfigKey.DEFAULT_ENCODING)
        logger.debug("use default encoding: {}".format(encoding))

    if typepy.is_null_string(proxy):
        proxy = app_config_manager.load().get(ConfigKey.PROXY_SERVER)

    con, is_create_db = create_database(ctx.obj[Context.OUTPUT_PATH], ctx.obj[Context.DUP_DATABASE])
    converter = UrlConverter(
        logger=logger,
        con=con,
        symbol_replace_value=ctx.obj[Context.SYMBOL_REPLACE_VALUE],
        index_list=ctx.obj.get(Context.INDEX_LIST),
        verbosity_level=ctx.obj.get(Context.VERBOSITY_LEVEL),
        format_name=format_name,
        encoding=encoding,
        proxy=proxy,
    )

    converter.convert(url)

    sys.exit(finalize(con, converter, is_create_db))


@cmd.command(epilog=COMMAND_EPILOG)
@click.argument("credentials", type=click.Path(exists=True))
@click.argument("title", type=str)
@click.pass_context
def gs(ctx, credentials, title):
    """
    Convert a spreadsheet in Google Sheets to a SQLite database file.

    CREDENTIALS: OAuth2 Google credentials file.
    TITLE: Title of the Google Sheets to convert.
    """

    logger = make_logger("{:s} gs".format(PROGRAM_NAME), ctx.obj[Context.LOG_LEVEL])
    con, is_create_db = create_database(ctx.obj[Context.OUTPUT_PATH], ctx.obj[Context.DUP_DATABASE])
    converter = GoogleSheetsConverter(
        logger=logger,
        con=con,
        symbol_replace_value=ctx.obj[Context.SYMBOL_REPLACE_VALUE],
        index_list=ctx.obj.get(Context.INDEX_LIST),
        verbosity_level=ctx.obj.get(Context.VERBOSITY_LEVEL),
    )

    converter.convert(credentials, title)

    sys.exit(finalize(con, converter, is_create_db))


@cmd.command()
@click.pass_context
def configure(ctx):
    """
    Configure the following application settings:

    (1) Default encoding to load files.
    (2) HTTP/HTTPS proxy server URI (for url sub-command).

    Configurations are written to '~/.sqlitebiter'.
    You can remove these settings by deleting '~/.sqlitebiter'.
    """

    logger = make_logger("{:s} file".format(PROGRAM_NAME), ctx.obj[Context.LOG_LEVEL])

    logger.debug(
        "{} configuration file existence: {}".format(PROGRAM_NAME, app_config_manager.exists)
    )

    try:
        sys.exit(app_config_manager.configure())
    except KeyboardInterrupt:
        click.echo()
        sys.exit(errno.EINTR)


@cmd.command(epilog=COMMAND_EPILOG)
@click.argument("shell", type=click.Choice(["bash", "zsh"]))
@click.pass_context
def completion(ctx, shell):
    """
    A helper command to setup command completion.

    To setup for bash:

        sqlitebiter completion bash >> ~/.bashrc

    To setup for zsh:

        sqlitebiter completion zsh >> ~/.zshrc
    """

    if shell == "bash":
        click.echo(
            dedent(
                """\
            _sqlitebiter_completion() {
                local IFS=$'
            '
                COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                            COMP_CWORD=$COMP_CWORD \
                            _SQLITEBITER_COMPLETE=complete $1 ) )
                return 0
            }

            _sqlitebiter_completionetup() {
                local COMPLETION_OPTIONS=""
                local BASH_VERSION_ARR=(${BASH_VERSION//./ })
                # Only BASH version 4.4 and later have the nosort option.
                if [ ${BASH_VERSION_ARR[0]} -gt 4 ] || ([ ${BASH_VERSION_ARR[0]} -eq 4 ] && [ ${BASH_VERSION_ARR[1]} -ge 4 ]); then
                    COMPLETION_OPTIONS="-o nosort"
                fi

                complete $COMPLETION_OPTIONS -F _sqlitebiter_completion sqlitebiter
            }
            """
            )
        )
    elif shell == "zsh":
        click.echo(
            dedent(
                """\
                _sqlitebiter_completion() {
                    local -a completions
                    local -a completions_with_descriptions
                    local -a response
                    response=("${(@f)$( env COMP_WORDS="${words[*]}" \
                                        COMP_CWORD=$((CURRENT-1)) \
                                        _SQLITEBITER_COMPLETE="complete_zsh" \
                                        sqlitebiter )}")

                    for key descr in ${(kv)response}; do
                    if [[ "$descr" == "_" ]]; then
                        completions+=("$key")
                    else
                        completions_with_descriptions+=("$key":"$descr")
                    fi
                    done

                    if [ -n "$completions_with_descriptions" ]; then
                        _describe -V unsorted completions_with_descriptions -U -Q
                    fi

                    if [ -n "$completions" ]; then
                        compadd -U -V unsorted -Q -a completions
                    fi
                    compstate[insert]="automenu"
                }

                compdef _sqlitebiter_completion sqlitebiter;
                """
            )
        )


if __name__ == "__main__":
    cmd()
