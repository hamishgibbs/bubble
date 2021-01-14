import os
import json
import random


def scaffold(file, template, tag=None):
    '''Function to scaffold a file from a template'''

    # Replace leading whitespace characters in block string, encode as bytes
    template = template.replace('        ', '')

    prompt_for_file_overwrite(file)

    try:

        if not tag:

            template = '# -- Template by bubble with <3. --\n\n' + template

        # Write template to file with bubble header.
        with open(file, 'w') as f:

            f.write(template)

        # Success message
        print('Successfully created %s. %s' % (file, random_success()))

    except Exception:

        # Raise exception for any issues writing template to file
        raise Exception('Unable to write new file %s/' % file)


def language(file):
    '''Get language from a file extension'''

    # Return arbitrary language for Makefile template
    # this will have to change for >1 makefile template
    if 'Makefile' in file:

        return('makefile')

    # Split filename string at ".", select end element
    extension = file.split('.')[-1]

    # Identify R files with ".r" or ".R" extension
    if extension in ['r', 'R']:

        return('r')

    # Identify Python files with ".py" extension
    elif extension in ['py']:

        return('py')

    # Raise error for unknown file extensions
    else:

        raise ValueError('Unknown file extension %s.' % extension)


def prompt_for_file_overwrite(file: str):

    # Prompt to overwrite an existing file
    if os.path.exists(file):

        overwrite = input('Found an existing file at %s.\nDo you want to overwrite this file? (Y/n) ' % file)

        if overwrite != 'Y':

            print('Stopping.')
            exit()


def write_bubble_config(root: str):

    fn = root + '/bubble.json'

    prompt_for_file_overwrite(fn)

    with open(fn, 'w') as f:

        json.dump({"extensions": [".py", ".R"], "watch_dirs": ["src"]}, f)


def get_bubble_config(root: str = os.getcwd()):

    try:

        with open(root + '/bubble.json', 'r') as f:

            config = json.load(f)

    except Exception as e:

        raise e

    return config


def random_success():

    success = ['\U0001F973', '\U0001F382', '\U0001F37E', '\U0001F389', '\U0001F38A']

    return(random.choice(success))


def flatten(list):

    return [item for sublist in list for item in sublist]
