# Copyright (c) 2018 UniquID

import click

from uniquid.commands.login import login
from uniquid.commands.login import logout
from uniquid.commands.login import status
from uniquid.commands.device import show_device
from uniquid.commands.device import list_devices
from uniquid.commands.contract import create_contracts
from uniquid.commands.contract import list_contracts
from uniquid.commands.contract import show_contract
from uniquid.commands.contract import delete_contracts
from uniquid.commands.share import list_shares
from uniquid.commands.share import create_shares
from uniquid.commands.share import delete_shares
from uniquid.commands.aliases import list_aliases
from uniquid.commands.deploy import deploy
import uniquid.core.constants as constants
import uniquid.commands.aliases as aliases


class AliasGroup(click.Group):
    """Sub-class of Group allows aliases to be defined for each of the
    commands.
    """
    def get_command(self, ctx, cmd_name):
        full_name = aliases.get_cmd_name(cmd_name)
        if full_name is None:
            full_name = cmd_name
        return click.Group.get_command(self, ctx, full_name)


# high-level grouping of all commands
@click.command(cls=AliasGroup)
@click.version_option(constants.APP_VERSION)
def cli_group():
    pass


# add each command to the high-level group
cli_group.add_command(list_aliases)
cli_group.add_command(login)
cli_group.add_command(logout)
cli_group.add_command(status)
cli_group.add_command(show_device)
cli_group.add_command(list_devices)
cli_group.add_command(create_contracts)
cli_group.add_command(list_contracts)
cli_group.add_command(show_contract)
cli_group.add_command(delete_contracts)
cli_group.add_command(list_shares)
cli_group.add_command(create_shares)
cli_group.add_command(delete_shares)
cli_group.add_command(deploy)

# configure aliases for the commands which have an alias
aliases.set_alias('li', login.name)
aliases.set_alias('lo', logout.name)
aliases.set_alias('st', status.name)
aliases.set_alias('la', list_aliases.name)
aliases.set_alias('sd', show_device.name)
aliases.set_alias('ld', list_devices.name)
aliases.set_alias('cc', create_contracts.name)
aliases.set_alias('lc', list_contracts.name)
aliases.set_alias('sc', show_contract.name)
aliases.set_alias('dc', delete_contracts.name)
aliases.set_alias('ls', list_shares.name)
aliases.set_alias('cs', create_shares.name)
aliases.set_alias('ds', delete_shares.name)
aliases.set_alias('dp', deploy.name)


if __name__ == '__main__':
    cli_group()
