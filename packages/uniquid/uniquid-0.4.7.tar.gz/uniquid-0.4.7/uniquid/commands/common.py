# Copyright (c) 2018 UniquID

import click


def print_error(in_string):
    """Print a string to stderr using click framework. Provides a platform
    independant way of printing to stderr to the core code.

        Arguments:
        in_string -- String.
    """
    click.echo(message=in_string, err=True)
