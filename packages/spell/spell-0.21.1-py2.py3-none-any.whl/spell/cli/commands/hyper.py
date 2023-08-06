# -*- coding: utf-8 -*-
import click

from spell.cli.exceptions import (
    api_client_exception_handler,
    ExitException,
    SPELL_INVALID_CONFIG,
)
from spell.cli.commands.run import create_run_request
from spell.cli.log import logger
from spell.cli.utils.parse_utils import ParseException, parse_grid_params
from spell.cli.utils import tabulate_rows, with_emoji, ellipses

from spell.cli.utils.command_options import (
    dependency_params,
    workspace_spec_params,
    machine_config_params,
    cli_params,
    description_param,
    docker_image_option,
    idempotent_option
)


@click.group(name="hyper", short_help="Create hyperparameter searches",
             help="Create hyperparameter searches on Spell")
@click.pass_context
def hyper(ctx):
    pass


@hyper.command(name="grid",
               short_help="Execute a hyperparameter grid search")
@click.argument("command")
@click.argument("args", nargs=-1)
@click.option("--param", "params", multiple=True, metavar='NAME=VALUE[,VALUE,VALUE,...]',
              help="Specify a hyperparameter for the run.  A run will be created for all "
                   "hyperparameter value combinations provided. NAME should appear in the "
                   "COMMAND surrounded by colons (i.e., \":NAME:\" to indicate where "
                   "the VALUEs should be substituted when creating each run.")
@idempotent_option
@machine_config_params
@docker_image_option
@dependency_params
@workspace_spec_params
@description_param
@cli_params
@click.pass_context
def grid(ctx, command, args, params, machine_type, pip_packages, requirements_file, apt_packages,
         docker_image, framework, python2, python3, commit_ref, description, envvars, raw_resources,
         conda_env, conda_file, force, verbose, local_caching, idempotent, **kwargs):
    """
    Execute a hyperparameter grid search for COMMAND remotely on Spell's infrastructure

    The grid command is used to create numerous runs simultaneously to perform a hyperparameter
    grid search. A run will be created for all possible combinations of parameters provided with
    the "--param" option.  All other options are the same as the spell run command and will apply
    to every run created in the hyperparameter search.
    """
    logger.info("starting hyper grid command")
    try:
        params = parse_grid_params(params)
    except ParseException as e:
        raise ExitException(click.wrap_text(
            "Incorrect formatting of param '{}', it must be NAME=VALUE[,VALUE,VALUE,...]".format(e.token)),
            SPELL_INVALID_CONFIG)
    run_req = create_run_request(ctx, command, args, machine_type, pip_packages, requirements_file, apt_packages,
                                 docker_image, framework, python2, python3, commit_ref, description, envvars,
                                 raw_resources, conda_env, conda_file, force, verbose, local_caching,
                                 idempotent, run_type="user")
    client = ctx.obj["client"]
    logger.info("sending hyper search request to api")
    with api_client_exception_handler():
        hyper = client.hyper_grid_search(params, run_req)
    utf8 = ctx.obj["utf8"]
    click.echo(with_emoji(u"💫", "Casting hyperparameter search #{}".format(hyper.id), utf8) + ellipses(utf8))

    # promote param names to attributes for tabulate
    for run in hyper.runs:
        run.id = str(run.id)
        for param in params:
            setattr(run, param, run.hyper_params[param])
    # display parameters and associated run IDs
    param_names = list(params.keys())
    headers = param_names + ["Run ID"]
    columns = list(params.keys()) + ["id"]
    tabulate_rows(hyper.runs, headers=headers, columns=columns)


# TODO(Brian): add hyper random command
