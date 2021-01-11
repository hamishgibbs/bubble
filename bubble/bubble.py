import os
import sys
from pathlib import Path
import click
from bubble.dockerfile import new_dockerfile
from bubble.template import templates
from bubble.utils import scaffold, language
from bubble.makefile import create_make_target

# SHOULD BE VERY SIMPLE

resource_package = __name__


@click.group()
def cli():
    """Entry point for the bubble cli."""


@cli.command()
@click.option("-root",
              "--root",
              default=os.getcwd(),
              help='Specify project root.')
def init(root: str = os.getcwd()):

    with open(root + '/bubble.json', 'w') as f:

        f.write('{"extensions":[".py", ".R"], "watch_dirs":["src"]}')


@cli.command()
@click.option("-f",
              "--file",
              help='File to create.')
@click.option("-t",
              "--tag",
              help='Omit bubble file tag.',
              is_flag=True)
def create(file: str,
           tag: bool):

    template = templates()[language(file)]

    scaffold(file, template, tag)



if __name__ == '__main__':

    cli()
