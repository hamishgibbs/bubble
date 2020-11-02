import os
import click
import pkg_resources
import re

#Maybe start over. Should be VERY simple
# get tests in place

# VERY SIMPLE

resource_package = __name__

#be careful of overwriting files
# use some regular expressions
#add way to sepcify proj dir from .env file in template

@click.command()
@click.option('-f', '--file', help='File path.')
@click.option('-t', '--template', help='Type of template.')
@click.option('-m', '--make_target', help='Generate a Makefile target.', is_flag=True)
# @click.option('-f', '--file', help='File to be parsed.')
def cli(file=None, template=None, make_target=None):
    """Entry point for the bubble cli."""

    # User must specify a template
    if template is None and make_target is None:

        raise ValueError('Please specify an action: -t template, -m makefile target.')

    elif file is not None and template is not None:

        scaffold(file, template)

    elif file is not None and make_target is not None:

        create_make_target(file)

    else:

        raise ValueError('Unknown input.')



def scaffold(file, template):
    '''Function to scaffold a file from a template'''

    if template not in ['csv', 'png', 'module']:

        raise ValueError('Unknown template. Please specify csv, png, or module.')

    templates = {'R': {'csv': 'templates/csv.R',
                       'png': 'templates/png.R',
                       'module': 'templates/module.R'},
                'PYTHON': {'csv': 'templates/csv.py',
                           'png': 'templates/png.py',
                           'module': 'templates/module.py'}

                }

    template_path = templates[language(file)][template]

    template = pkg_resources.resource_string(resource_package,
                                             template_path)

    if os.path.exists(file):

        overwrite = input('Found an existing file at %s. \nDo you want to overwrite this file? (Y/n)' % file)

        if overwrite != 'Y':

            print('Stopping.')
            exit()

    try:

        with open(file, 'wb') as f:

            f.write(b'# -- Template by bubble with <3. --\n\n' + template)

        print('Successfully created %s.' % file)

    except:

        raise Exception('Unable to write new file %s/' % file)


def language(file):
    '''Get language from a file extension'''

    extension = file.split('.')[-1]

    if extension in ['r', 'R']:

        return('R')

    elif extension in ['py']:

        return('PYTHON')

    else:

        raise ValueError('Unknown file extension .%' % extension)

def create_make_target(file):
    '''
    Function to parse a template file and create a makefile target
    '''

    if not os.path.exists(file):

        raise FileNotFoundError('File not found.')

    if not os.path.exists('Makefile'):

        raise FileNotFoundError('No Makefile found in current directory.')

    with open('Makefile') as m:

        makefile_lines = m.readlines()

    with open(file) as m:

        file_lines = m.readlines()

    target_name = file.split('.')[0].split('/')[-1]

    '''
    Identify existing targets with the same name in the makefile.

    If present, prompt user about updating it.

    If updating, remove the existing target from the Makefile. The new target
    will be appended to the end of the file.

    Future: add target in place.

    '''

    existing_targets = get_existing_targets(makefile_lines)

    if target_name in existing_targets:

        response = input('Found an existing target %s. Do you want to update it? (Y/n) ' % target_name)

        if response != 'Y':

            print('Stopping.')
            exit()

        else:

            remove_existing_target(file, target_name, makefile_lines)

    in_quotes = re.compile('\"(.+?)\"')

    if language(file) == 'R':

        args = capture_args_r(file_lines)

        args = flatten([in_quotes.findall(x) for x in args])

        args = ['${PWD}/' + x for x in args]

        depends = args[:-1]

    if language(file) == 'PYTHON':

        args = capture_args_py(file_lines)

        args = flatten([in_quotes.findall(x) for x in args])

        args = ['${PWD}/' + x for x in args]

        depends = args[1:-1]

    # Target is the last interactive arg
    target = args[-1]

    depends = ' \n'.join(depends)

    short_target = target_name + ': ' + target + '\n\n'

    target = target + ': ${PWD}/' + file + ' \\ ' + '\n' + '\t' + depends + '\n\t$(%s_INTERPRETER) $^ $@'  % language(file)

    # Append this target to the makefile
    makefile_content = ''.join(makefile_lines) + '\n\n' + short_target + target

    with open('Makefile', 'w') as m:

        m.write(makefile_content)

    print('Successfully updated Makefile target "%s".' % target_name)


def capture_args_r(file_lines):
    '''Capture arguments from an R template'''

    capture_start = file_lines.index('if(interactive()){\n')

    capture_stop = file_lines.index('}\n')

    args = file_lines[capture_start + 1: capture_stop - 2]

    return(args)


def capture_args_py(file_lines):
    '''Capture arguments from a Python template'''

    capture_start = file_lines.index('if not hasattr(main, "__file__"):\n')

    capture_stop = file_lines.index('    ]\n')

    args = file_lines[capture_start + 1: capture_stop]

    return(args)


def get_existing_targets(makefile_lines):
    '''Get existing targets from a makefile'''

    return(flatten([re.compile('(.+?):').findall(x) for x in makefile_lines]))


def remove_existing_target(file, target_name, makefile_lines):
    '''
    Function to remove a target from a makefile

    Identifies start of target at `NAME:`

    Identifies end of target at `$(LANGUAGE_INTERPRETER) $^ $@`
    '''

    # Get line index of the start of the target
    existing_index = [re.compile(target_name + ':').findall(x) for x in makefile_lines]

    # Target names should not be duplicated - makefile should throw error if they are
    existing_index = [i for i, x in enumerate(existing_index) if x == [target_name + ':']][0]

    # Get index of the end of the target by finding all relevant interpreters
    interpreter_index = [i for i, x in enumerate(makefile_lines) if '$(%s_INTERPRETER) $^ $@'  % language(file) in x]

    # Select the first interpreter following the start of the target
    interpreter_index = [x for x in interpreter_index if x > existing_index][0]

    # Remove these lines from the makefile
    del makefile_lines[existing_index - 2:interpreter_index + 1]

def flatten(list):

    return [item for sublist in list for item in sublist]



if __name__ == '__main__':

    cli()
