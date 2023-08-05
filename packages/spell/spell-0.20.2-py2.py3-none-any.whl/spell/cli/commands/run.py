# -*- coding: utf-8 -*-
import os

import click
import git
import requirements

from spell.api.runs_client import RunRequest
from spell.cli.api_constants import (
    get_machine_types,
    get_machine_type_default,
    get_frameworks,
)
from spell.cli.exceptions import (
    api_client_exception_handler,
    ExitException,
    SPELL_INVALID_CONFIG,
)
from spell.cli.commands.logs import logs
from spell.cli.log import logger
from spell.cli.utils import LazyChoice, git_utils, parse_utils, HiddenOption, with_emoji, ellipses
from spell.cli.utils.parse_utils import ParseException


@click.command(name="run",
               short_help="Execute a new run")
@click.argument("command")
@click.argument("args", nargs=-1)
@click.option("-t", "--machine-type",
              type=LazyChoice(get_machine_types), default=get_machine_type_default,
              help="Machine type to run on")
@click.option("--pip", "pip_packages",
              help="Single dependency to install using pip", multiple=True)
@click.option("--pip-req", "requirements_file",
              help="Requirements file to install using pip")
@click.option("--apt", "apt_packages",
              help="Dependency to install using apt", multiple=True)
@click.option("--from", "docker_image",
              help="Dockerfile on docker hub to run from")
@click.option("--framework",
              help="Machine learning framework to use. Can specify specific version"
              " with ==, e.g. --framework pytorch==0.2.0. For a full list of"
              " available frameworks see https://spell.run/docs/customizing_environments")
@click.option("--python2", is_flag=True,
              help="set python version to python 2")
@click.option("--python3", is_flag=True,
              help="set python version to python 3 (default)")
@click.option("--conda-env", help="Name of conda environment name to activate. "
                                  "If omitted but --conda-file is specified then it is "
                                  "assumed that --conda-file is an 'explicit' env file.")
@click.option("--conda-file",
              help="Path to conda environment file, defaults to ./environment.yml "
                   "when --conda-env is specified",
              type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=False, readable=True),
              default=None)
@click.option("-b", "--background", is_flag=True,
              help="Do not print logs")
@click.option("-c", "--commit-ref", default="HEAD",
              help="Git commit hash to run")
@click.option("-d", "--description", default=None,
              help="Description of the run. If unspecified defaults to the current commit message")
@click.option("-e", "--env", "envvars", multiple=True,
              help="Add an environment variable to the run")
@click.option("-m", "--mount", "raw_resources", multiple=True, metavar='RESOURCE[:MOUNT_PATH]',
              help="Attach a resource file or directory to the run (e.g., from a run output, public dataset, "
                   "or upload). The resource (specified by a Spell resource path) is required. An optional mount path "
                   "within the container can also be specified, separated by a colon from the resource name. "
                   "If the mount path is omitted, it defaults to the base name of the resource (e.g., "
                   "'mnist' for 'public/image/mnist'). "
                   "Example: --mount runs/42:/mnt/data")
@click.option("-f", "--force", is_flag=True,
              help="Skip interactive prompts")
@click.option("-v", "--verbose", is_flag=True,
              help="Print additional information")
@click.option("--local_caching", cls=HiddenOption, is_flag=True, help="enable local caching of attached resources")
@click.option("--idempotent", cls=HiddenOption, is_flag=True,
              help="Use an existing identical run if one is found instead of launching a new one")
@click.pass_context
def run(ctx, command, args, machine_type, pip_packages, requirements_file, apt_packages,
        docker_image, framework, python2, python3, commit_ref, description, envvars, raw_resources, background,
        conda_env, conda_file, force, verbose, local_caching, idempotent, run_type="user", **kwargs):
    """
    Execute COMMAND remotely on Spell's infrastructure

    The run command is used to create runs and is likely the command you'll use most
    while using Spell. It is intended to be emulate local development. Any code,
    software, binaries, etc., that you can run locally on your computer can be run
    on Spell - you simply put `spell run` in front of the same commands you would use
    locally and they will run remotely. The various options can be used to customize
    the environment in which COMMAND will run.
    """
    logger.info("starting run command")

    run_req = create_run_request(ctx, command, args, machine_type, pip_packages, requirements_file, apt_packages,
                                 docker_image, framework, python2, python3, commit_ref, description, envvars,
                                 raw_resources, background, conda_env, conda_file, force, verbose, local_caching,
                                 idempotent, run_type)

    # execute the run
    client = ctx.obj["client"]
    logger.info("sending run request to api")
    with api_client_exception_handler():
        run = client.run(run_req)

        # Stash run metadata in the context so that the jupyter command can use it
        ctx.meta["run"] = run
        ctx.meta["root_directory"] = run_req.root_directory
        ctx.meta["local_root"] = run_req.local_root

    utf8 = ctx.obj["utf8"]
    if run.already_existed:
        click.echo(with_emoji(u"♻️", "Idempotent: Found existing run {}".format(run.id), utf8) + ellipses(utf8))
    else:
        click.echo(with_emoji(u"💫", "Casting spell #{}".format(run.id), utf8) + ellipses(utf8))
    if background:
        click.echo("View logs with `spell logs {}`".format(run.id))
    else:
        click.echo(with_emoji(u"✨", "Stop viewing logs with ^C", utf8))
        ctx.invoke(logs, run_id=str(run.id), follow=True, verbose=verbose, run_warning=True)


def create_run_request(ctx, command, args, machine_type, pip_packages, requirements_file, apt_packages,
                       docker_image, framework, python2, python3, commit_ref, description, envvars,
                       raw_resources, background, conda_env, conda_file, force, verbose, local_caching,
                       idempotent, run_type):
    framework_version = None
    if framework is not None:
        split = framework.split("==")
        framework = LazyChoice(get_frameworks).convert(split[0],
                                                       None, ctx)
        framework_version = split[1] if len(split) > 1 else None

    if command is None:
        cmd_with_args = None
    else:
        cmd_with_args = " ".join((command,) + args)

    git_repo = None
    try:
        git_repo = git.Repo(os.getcwd(), search_parent_directories=True)
    except git.exc.InvalidGitRepositoryError:
        pass
    if git_repo is None:
        if force:
            logger.warn("No git repository found! Running without a workspace.")
        else:
            click.confirm("Could not find a git repository, so no user files will be available "
                          "in the run. Continue anyway?", default=True, abort=True)
        local_root = None
        workspace_id = None
        commit_hash = None
        relative_path = None
        root_directory = None
    else:
        # Get relative path from git-root to CWD.
        local_root = git_repo.working_dir
        relative_path = os.path.relpath(os.getcwd(), local_root)
        root_directory = os.path.basename(local_root)

        workspace_id, commit_hash, commit_message = git_utils.push_workspace(ctx, git_repo, commit_ref, force=force)
        if description is None:
            description = commit_message

    source_spec = sum(1 for x in (framework, docker_image, conda_env) if x is not None)
    if source_spec > 1:
        raise ExitException("Only one of the following options can be specified: --framework, --from, --conda-env",
                            SPELL_INVALID_CONFIG)

    if docker_image is not None and (pip_packages or apt_packages or requirements_file):
        raise ExitException("--apt, --pip, or --pip-req cannot be specified when --from is provided."
                            " Please install packages from the specified Dockerfile.",
                            SPELL_INVALID_CONFIG)

    if conda_env is not None and conda_file is None:
        if not os.path.exists("environment.yml"):
            raise ExitException("Default value for \"--conda-file\" invalid: Path \"environment.yml\" does not exist.",
                                SPELL_INVALID_CONFIG)
        conda_file = os.path.join(os.getcwd(), "environment.yml")
    if conda_env is not None and (pip_packages or requirements_file):
        raise ExitException("--pip or --pip-req cannot be specified when using a conda environment. "
                            "You can include the pip installs in the conda environment file instead.")
    if conda_env is not None and (python2 or python3):
        raise ExitException("--python2 or --python3 cannot be specified when using a conda environment. "
                            "Please include the python version in your conda environment file instead.")
    # Read the conda environment file
    conda_env_contents = None
    if conda_file is not None:
        with open(conda_file) as conda_f:
            conda_env_contents = conda_f.read()

    if requirements_file:
        pip_packages = list(pip_packages)
        with open('requirements.txt', 'r') as rf:
            for req in requirements.parse(rf):
                pip_packages.append(req.line)

    if python2 and python3:
        raise ExitException("--python2 and --python3 cannot both be specified")

    # extract envvars into a dictionary
    curr_envvars = parse_utils.parse_env_vars(envvars)

    # extract attached resources
    try:
        attached_resources = parse_utils.parse_attached_resources(raw_resources)
    except ParseException as e:
        raise ExitException(click.wrap_text(
            "Incorrect formatting of mount '{}', it must be <resource_path>[:<mount_path>]".format(e.token)),
            SPELL_INVALID_CONFIG)

    return RunRequest(
        machine_type=machine_type,
        command=cmd_with_args,
        workspace_id=workspace_id,
        commit_hash=commit_hash,
        cwd=relative_path,
        root_directory=root_directory,
        pip_packages=pip_packages,
        apt_packages=apt_packages,
        docker_image=docker_image,
        framework=framework,
        framework_version=framework_version,
        python2=python2 if (python2 or python3) else None,
        description=description,
        envvars=curr_envvars,
        attached_resources=attached_resources,
        conda_file=conda_env_contents,
        conda_name=conda_env,
        local_caching=local_caching,
        run_type=run_type,
        idempotent=idempotent,
        local_root=local_root,
    )
