import os
import click
import pkg_resources
import re
from template import templates
from dockerfile import new_dockerfile
from utils import scaffold, random_success
from makefile import create_make_target
import textwrap
import random

# SHOULD BE VERY SIMPLE

resource_package = __name__

@click.command()
@click.option('-f', '--file', help='File path.')
@click.option('-t', '--template', help='Type of template.')
@click.option('-m', '--make_target', help='Generate a Makefile target.', is_flag=True)
@click.option('-d', '--dockerfile', help='Generate a Dockerfile.')
@click.option('-p', '--project', help='Generate a project.')
# @click.option('-f', '--file', help='File to be parsed.')
def cli(file=None, template=None, make_target=None, dockerfile=None, project=None):
    """Entry point for the bubble cli."""

    # User must specify a template
    if project is not None:

        new_project(project)

    elif template is None and make_target is None:

        raise ValueError('Please specify an action: -t template, -m makefile target.')

    elif file is not None and template is not None:

        scaffold(file, template)

    elif file is not None and make_target is not None:

        create_make_target(file)

    elif file is None and make_target is not None and dockerfile is None:

        scaffold('Makefile', 'makefile')

    elif dockerfile is not None:

        new_dockerfile(dockerfile)

    else:

        raise ValueError('Unknown input.')


def new_project(project):
    '''Function to scaffold a new project from scratch'''

    proj_name = os.getcwd().split('/')[-1]

    os.mkdir('src')
    os.mkdir('src/data')
    os.mkdir('src/analysis')
    os.mkdir('src/vis')

    os.mkdir('data')
    os.mkdir('data/raw')
    os.mkdir('data/interim')
    os.mkdir('data/processed')

    os.mkdir('output')
    os.mkdir('output/figs')

    scaffold('Makefile', 'makefile')

    new_dockerfile(project)

    print('Successfully created project %s. %s' % (proj_name, random_success()))

if __name__ == '__main__':

    cli()
