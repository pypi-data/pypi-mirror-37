# -*- coding: utf-8 -*-

"""Console script for flattenit."""
import sys
import click
from flattenit.flattenit import flattenit


@click.command()
def main(args=None):
    """Console script for flattenit."""
    # click.echo("Replace this message by putting your code into "
    #            "flattenit.cli.main")
    # click.echo("See click documentation at http://click.pocoo.org/")
    matrix = [[1, 2, 3], [4, 5, 6]]
    new_list = flattenit(matrix)
    print('Input matrix is {}'.format(matrix))
    print('Output list is {}'.format(new_list))
    return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
