# Copyright (c) 2018 UniquID

import click
from uniquid.core.login_manager import LoginManager
from uniquid.core.cli_console import CliConsole
from uniquid.core.deploy import Deploy
import uniquid.commands.common as common


@click.command(name='deploy')
@click.argument('platform',
                nargs=1,
                required=True)
def deploy(platform):
    """Deploy Uniquid security components to platform PLATFORM."""
    cc = CliConsole(click.echo, common.print_error,
                    'text', click.ClickException,
                    click.confirm, click.prompt)
    lm = LoginManager(cc)
    deploy = Deploy(cc, lm)
    deploy.deploy(platform)
