# -*- coding: utf-8 -*-

"""Console script for simple_jsondiff."""
import sys
import click

from simple_jsondiff import jsondiff


@click.command()
@click.argument('first', type=click.File('rb'))
@click.argument('second', type=click.File('rb'))
def main(first, second):
    """Console script for simple_jsondiff."""
    click.echo(jsondiff(first.read(), second.read()))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
