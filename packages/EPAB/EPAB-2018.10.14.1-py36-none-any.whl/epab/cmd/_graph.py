# coding=utf-8
"""
Wrapper around pyreverse (needs Graphviz in the path)
"""
from pathlib import Path

import click
import elib_run

from epab.core import config


def _graph():
    out_files = [
        Path(f'packages_{config.PACKAGE_NAME()}.png'),
        Path(f'classes_{config.PACKAGE_NAME()}.png'),

    ]
    elib_run.run(f'pyreverse -o png -p {config.PACKAGE_NAME()} {config.PACKAGE_NAME()}')
    if any((file.exists() for file in out_files)):
        out_dir = Path('graphs')
        out_dir.mkdir(exist_ok=True)
        for file in out_files:
            if file.exists():
                file.rename(f'{file.parent}/graphs/{file.name}')


@click.command()
def graph():
    """
    Creates a graphical representation of the package inheritance & import trees
    """
    _graph()
