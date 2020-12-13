import os
import random
from bubble.template import templates


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


def random_success():

    success = ['\U0001F973', '\U0001F382', '\U0001F37E', '\U0001F389', '\U0001F38A']

    return(random.choice(success))


def flatten(list):

    return [item for sublist in list for item in sublist]
