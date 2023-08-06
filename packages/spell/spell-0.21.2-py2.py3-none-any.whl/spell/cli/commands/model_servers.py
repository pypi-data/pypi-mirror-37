import click
import re

from spell.cli.log import logger
from spell.cli.exceptions import api_client_exception_handler, ExitException
from spell.cli.utils import HiddenOption, tabulate_rows, convert_to_local_time


@click.group(name="model-servers", short_help="Manage model servers",
             help="""Manage model servers

             With no subcommand, displays all of your model servers""",
             invoke_without_command=True)
@click.option("--raw", help="display output in raw format", is_flag=True, default=False,
              cls=HiddenOption)
@click.pass_context
def model_servers(ctx, raw):
    if not ctx.invoked_subcommand:
        client = ctx.obj["client"]
        with api_client_exception_handler():
            model_servers = client.get_model_servers()
        if len(model_servers) == 0:
            click.echo("There are no model servers to display.")
        else:
            data = [(ms.get_full_name(), ms.url, ms.status, ms.get_age()) for ms in model_servers]
            tabulate_rows(data,
                          headers=["NAME", "URL", "STATUS", "AGE"],
                          raw=raw)


@model_servers.command(name="create", short_help="Create a new model server",
                       help="""Create a new Tensorflow model server with the specified NAME from
                       resources stored at PATH. NAME should be fully qualified, following the
                       format: <model_name>:<tag>""")
@click.pass_context
@click.argument("name")
@click.argument("path")
def create(ctx, name, path):
    server_name, tag = get_name_and_tag(name)
    client = ctx.obj["client"]
    with api_client_exception_handler():
        model_server = client.new_model_server(server_name=server_name, tag=tag, path=path)
    logger.info("Successfully created model server: {}".format(model_server.get_full_name()))


@model_servers.command(name="rm", short_help="Remove a model server",
                       help="""Remove the model server with the specified NAME""")
@click.pass_context
@click.argument("name")
def remove(ctx, name):
    server_name, tag = get_name_and_tag(name)
    client = ctx.obj["client"]
    with api_client_exception_handler():
        client.delete_model_server(server_name=server_name, tag=tag)
    logger.info("Succesfully removed model server {}".format(name))


@model_servers.command(name="start", short_help="Start a model server",
                       help="""Start the model server with the specified NAME""")
@click.pass_context
@click.argument("name")
def start(ctx, name):
    server_name, tag = get_name_and_tag(name)
    client = ctx.obj["client"]
    with api_client_exception_handler():
        client.start_model_server(server_name=server_name, tag=tag)
    logger.info("Succesfully started model server {}".format(name))


@model_servers.command(name="stop", short_help="Stop a model server",
                       help="""Stop the model server with the specified NAME""")
@click.pass_context
@click.argument("name")
def stop(ctx, name):
    server_name, tag = get_name_and_tag(name)
    client = ctx.obj["client"]
    with api_client_exception_handler():
        client.stop_model_server(server_name=server_name, tag=tag)
    logger.info("Succesfully stopped model server {}".format(name))


@model_servers.command(name="info", short_help="Get info about a model server",
                       help="""Get info about the model server with the specified NAME""")
@click.pass_context
@click.argument("name")
def get(ctx, name):
    server_name, tag = get_name_and_tag(name)
    client = ctx.obj["client"]
    with api_client_exception_handler():
        ms = client.get_model_server(server_name=server_name, tag=tag)

    lines = []
    lines.append(('Model Name', ms.server_name))
    lines.append(('Model Tag', ms.tag))
    lines.append(('Date Created', convert_to_local_time(ms.created_at)))
    lines.append(('Status', ms.status))
    lines.append(('Time Running', ms.get_age()))
    lines.append(('URL', ms.url))
    lines.append(('Access Token', ms.access_token))

    tabulate_rows(lines)


def get_name_and_tag(specifier):
    name_tag = specifier.split(":")
    if len(name_tag) != 2:
        raise ExitException("Invalid specifier {}. Expected <name>:<tag> format.".format(specifier))
    name, tag = name_tag[0], name_tag[1]
    if not is_valid_specifier_part(name) or not is_valid_specifier_part(tag):
        raise ExitException("Invalid specifier {}".format(specifier))
    return (name, tag)


def is_valid_specifier_part(part):
    return re.match("^\w+[\w\.-]*", part)
