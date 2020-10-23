import os
import shutil

def parse_fn(fn):
    '''Function to parse an input file path'''

    file_name = fn.split('/')[-1]

    path = '/'.join(fn.split('/')[:-1])

    extension = fn.split('.')[-1]

    print(extension)

    extensions = {
        'R': ['r', 'R'],
        'Python': ['py']
    }

    if extension in extensions['R']:

        language = 'R'

    elif extension in extensions['Python']:

        language = 'Python'

    else:

        file_types = ', '.join([item for sublist in extensions.values() for item in sublist])

        raise ValueError('Unknown file type. Bubble currently supports %s' % file_types)

    res = {
        'fn': file_name,
        'path': path,
        'language': language
    }

    return(res)


def write_template(template: str, fn: str):

    if fn['path'] == '':

        new_location = fn['fn']

    else:

        new_location = fn['path'] + '/' + fn['fn']

    if os.path.isabs(new_location):

        with open(new_location, 'wb') as f:

            f.write(template)

        print(new_location)

        write_success(new_location)

    else:

        new_location = os.getcwd() + '/' + new_location

        print(new_location)

        with open(new_location, 'wb') as f:

            f.write(template)

        write_success(new_location)


def write_success(new_location):

    print('Success. Created %s' % new_location)
