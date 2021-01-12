import os
import json
import click
from bubble.dockerfile import new_dockerfile
from bubble.template import templates
from bubble import utils
from bubble import makefile

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

    utils.write_bubble_config(root)


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

    template = templates()[utils.language(file)]

    utils.scaffold(file, template, tag)


@cli.command()
@click.option("-root",
              "--root",
              default=os.getcwd(),
              help='Specify project root.')
def make(root: str = os.getcwd()):

    config = utils.get_bubble_config(root)

    watch_dirs = [root + '/' + path for path in config['watch_dirs']]

    make_files = []

    for extension in config['extensions']:

        make_files.append(utils.flatten([makefile.find_files_to_be_made(path, extension) for path in watch_dirs]))

    new_targets = [makefile.make_target(x) for x in utils.flatten(make_files)]

    makefile.update_makefile(new_targets, root)


if __name__ == '__main__':

    cli()
