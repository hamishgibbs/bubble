import os
import click
import pkg_resources
import re
from template import templates
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


def scaffold(file, template, lang = None):
    '''Function to scaffold a file from a template'''

    if template not in ['csv', 'png', 'module', 'makefile', 'dockerfile']:

        raise ValueError('Unknown template. Specify csv, png, module, makefile, or dockerfile.')

    if lang is None:

        lang = language(file)

    # Access the appropriate template generator by langauge and template name
    template = templates()[lang][template]

    # Replace leading whitespace characters in block string, encode as bytes
    template = template().replace('        ', '').encode()

    # Prompt to overwrite an existing file
    if os.path.exists(file):

        overwrite = input('Found an existing file at %s.\nDo you want to overwrite this file? (Y/n)' % file)

        if overwrite != 'Y':

            print('Stopping.')
            exit()

    try:

        # Write template to file with bubble header.
        with open(file, 'wb') as f:

            f.write(b'# -- Template by bubble with <3. --\n\n' + template)

        # Success message
        print('Successfully created %s. %s' % (file, random_success()))

    except:

        # Raise exception for any issues writing template to file
        raise Exception('Unable to write new file %s/' % file)


def language(file):
    '''Get language from a file extension'''

    # Return arbitrary language for Makefile template
    # this will have to change for >1 makefile template
    if 'Makefile' in file:

        return('PYTHON')

    # Split filename string at ".", select end element
    extension = file.split('.')[-1]

    # Identify R files with ".r" or ".R" extension
    if extension in ['r', 'R']:

        return('R')

    # Identify Python files with ".py" extension
    elif extension in ['py']:

        return('PYTHON')

    # Raise error for unknown file extensions
    else:

        raise ValueError('Unknown file extension .%' % extension)


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


def new_dockerfile(dockerfile):

    scaffold('Dockerfile', 'dockerfile', dockerfile)

    proj_name = os.getcwd().split('/')[-1]

    # Check that Makefile exists in PWD
    if not os.path.exists('Makefile'):

        raise FileNotFoundError('No Makefile found in current directory.')

    # Read makefile lines
    with open('Makefile') as m:

        makefile_lines = m.readlines()

    insert_index = [i + 5 for i, x in enumerate(makefile_lines) if x == 'ifneq (,$(wildcard ./.env))\n']

    if dockerfile == 'PYTHON':

        target = dockerfile_target_py(proj_name)

    elif dockerfile == 'R':

        target = dockerfile_target_r(proj_name)

    else:

        raise ValueError('Unknown dockerfile language. Please choose PYTHON or R')

    makefile_lines.insert(insert_index[0], target)

    makefile_content = ''.join(makefile_lines)

    with open('Makefile', 'w') as m:

        m.write(makefile_content)

    # Success message
    print('Successfully added makefile targets. %s' % random_success())


def dockerfile_target_py(proj_name):

    build = 'build:\n\tdocker build . -t %s\n\n' % proj_name

    bash = 'bash:\n\tdocker run -it --rm --mount type=bind,source=${PWD},target=/usr/proj/ %s bash\n\n' % proj_name

    return(build + bash)


def dockerfile_target_r(proj_name):

    build = 'build:\n\tdocker build . -t %s\n\n' % proj_name

    up = 'up:\n\tdocker run -d -p 8787:8787 --mount type=bind,source=${PWD},target=/usr/proj/ --name %s -e USER=%s -e PASSWORD=%s %s\n\n' % (proj_name, proj_name, proj_name, proj_name)

    return(build + up)


def create_make_target(file, index = None):
    '''
    Function to parse a template file and create a makefile target
    '''

    # Check that file is accessible from PWD
    if not os.path.exists(file):

        raise FileNotFoundError('File not found.')

    # Check that Makefile exists in PWD
    if not os.path.exists('Makefile'):

        raise FileNotFoundError('No Makefile found in current directory.')

    # Read makefile lines
    with open('Makefile') as m:

        makefile_lines = m.readlines()

    # Read file lines
    with open(file) as m:

        file_lines = m.readlines()

    # Name target the same as file, "plot.R" -> "plot"
    target_name = file.split('.')[0].split('/')[-1]

    '''
    Identify existing targets with the same name in the makefile.

    If present, prompt user about updating it.

    If updating, remove the existing target from the Makefile. The new target
    will be appended to the end of the file.

    Future: add target in place.

    '''

    # Get a list of existing makefile targets
    existing_targets = get_existing_targets(makefile_lines)

    # Prompt about overwriting an existing target
    if target_name in existing_targets:

        response = input('Found an existing target %s. Do you want to update it? (Y/n) ' % target_name)

        if response != 'Y':

            print('Stopping.')
            exit()

        else:

            index = exiting_target_index(file, target_name, makefile_lines)

            remove_existing_target(makefile_lines, index['start'], index['end'])

    # Expression to capture text within double quotes
    in_quotes = re.compile('\"(.+?)\"')

    # capture arguments from R file
    if language(file) == 'R':

        args = capture_args_r(file_lines)

        args = flatten([in_quotes.findall(x) for x in args])

        # replace absolute paths with ${PWD} if present
        args = ['${PWD}/' + x.replace(os.getcwd() + '/', '') for x in args]

        depends = args[:-1]

    if language(file) == 'PYTHON':

        args = capture_args_py(file_lines)

        args = flatten([in_quotes.findall(x) for x in args])

        # replace absolute paths with ${PWD} if present
        args = ['${PWD}/' + x.replace(os.getcwd() + '/', '') for x in args]

        depends = args[1:-1]

    # Target is the last interactive arg
    target = args[-1]

    depends = '\\ \n\t'.join(depends)

    short_target = target_name + ': ' + target + '\n\n'

    target = target + ': ${PWD}/' + file + ' \\ ' + '\n' + '\t' + depends + '\n'

    if index is not None:

        # Append this target to the makefile
        makefile_lines.insert(index['start'], short_target + target)

        makefile_content = ''.join(makefile_lines)

    else:

        # Append this target to the makefile
        makefile_content = ''.join(makefile_lines) + '\n\n' + short_target + \
                           target + '\t$(%s_INTERPRETER) $^ $@'  % language(file)

    with open('Makefile', 'w') as m:

        m.write(makefile_content)

    print('Successfully updated Makefile target "%s". %s' % (target_name, random_success()))


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

    # Identify any targets matching the pattern "[TARGET]:"
    return(flatten([re.compile('(.+?):').findall(x) for x in makefile_lines]))

def exiting_target_index(file, target_name, makefile_lines):
    '''
    Function to extract the line indices of an existing Makefile target

    Identifies start of target at `NAME:`

    Identifies end of target at `$([LANGUAGE]_INTERPRETER) $^ $@`
    '''

    # Match target expression in Makefile
    existing_index = [re.compile(target_name + ':').findall(x) for x in makefile_lines]

    existing_index = [i for i, x in enumerate(existing_index)
                      if x == [target_name + ':']][0]

    # Get index of the end of the target by finding all relevant interpreters
    interpreter_index = [i for i, x in enumerate(makefile_lines) if '$(%s_INTERPRETER) $^ $@'  % language(file) in x]

    # Select the first interpreter following the start of the target
    interpreter_index = [x for x in interpreter_index if x > existing_index][0]

    return({'start': existing_index, 'end': interpreter_index})

def remove_existing_target(makefile_lines, start, end):
    '''
    Function to remove a target from a makefile
    '''

    # Delete lines between index from the makefile
    del makefile_lines[start:end]


def random_success():

    success = ['\U0001F973', '\U0001F382', '\U0001F37E', '\U0001F389', '\U0001F38A']

    return(random.choice(success))


def flatten(list):

    return [item for sublist in list for item in sublist]

if __name__ == '__main__':

    cli()
