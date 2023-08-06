# -*- coding: utf-8 -*-

"""Console script for magic-marker."""
# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import absolute_import
from magic_marker.magic_marker import MagicMarker
import sys
import click


# ======================================================================================================================
# Main
# ======================================================================================================================
@click.command()
@click.option('--config',
              is_flag=False,
              default=None,
              help='Path to the config file that will be the authoritative config source.')
@click.argument('test_path', type=click.Path(exists=True))
def main(test_path, config):
    """Automatically fix tests that are not marked with a UUID.

    \b
    Required Arguments:
        test_path               the path to pass to flake8
    """

    try:
        mm = MagicMarker()
        message = mm.run_flake8_and_mark(test_path, config)
        click.echo(click.style("\nSuccess!", fg='green'))
        click.echo(click.style("\nA backup was created : {}".format(mm.backup_path), fg='green'))
        click.echo(click.style(message, fg='green'))
    except RuntimeError as e:
        click.echo(click.style(str(e), fg='red'))
        click.echo(click.style("\nFailed!", fg='red'))

        sys.exit(1)


if __name__ == "__main__":
    main()  # pragma: no cover
