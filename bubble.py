import os
import click
import utils
import pkg_resources

resource_package = __name__


@click.command()
@click.option('-n', '--new', help='File path of a new file to scaffold.')
@click.option('-t', '--template', help='Type of template.')
def cli(new=None, template=None):
    """Entry point for the bubble cli."""

    # User must specify a template
    if new is not None and template is None:

        raise ValueError('Please specify a template.')

    if new is not None:

        scaffold(new, template)


    print(new, template)


if __name__ == '__main__':
    cli()

def scaffold(new, template):
    '''Function to scaffold a new file from a given template'''

    fn = utils.parse_fn(new)

    cwd = os.getcwd()

    templates = {'R': {'csv': 'templates/csv.R',
                       'png': 'templates/png.R',
                       'module': 'templates/module.R'},
                'Python': {'csv': 'templates/csv.py',
                           'png': 'templates/png.py',
                           'module': 'templates/module.py'}
                }

    template_path = templates[fn['language']][template]

    template = pkg_resources.resource_string(resource_package,
                                             template_path)

    if template in ['csv', 'png', 'module']:

        utils.write_template(template, fn)

    else:

        raise ValueError('Unknown template. Please specify csv, png, or module.')
