import os
import re
from bubble.utils import language, flatten, random_success


def should_be_made(fn):

    with open(fn, 'r') as f:

        file_content = f.read()

    if '# *** bubble make ***' in file_content:

        return True

    else:

        return False


def find_files(path: str = os.getcwd(),
               extension: str = '.py') -> list:
    """Search recursively for files matching a given extension.

    Args:
        path (str): Root path to search.
        extension (str): File extension to search for.

    Returns:
        list: List of matching files.

    """

    files = [os.path.join(dp, f) for
             dp, dn, filenames in os.walk(path) for
             f in filenames if os.path.splitext(f)[1] == extension]

    return(files)


def find_files_to_be_made(path,
                          extension):

    files = find_files(path, extension)

    need_making = [should_be_made(fn) for fn in files]

    files_to_make = [fn for i, fn in enumerate(files) if need_making[i]]

    return files_to_make


def get_bubble_template_dependencies(fn,
                                     input_start_str = '# *** bubble input start ***',
                                     input_end_str = '# *** bubble input end ***'):
    # get deps from a file - last will be output

    with open(fn, 'r') as f:

        file_content = f.readlines()

    start_index = [i for i, v in enumerate(file_content) if input_start_str in v][0]

    end_index = [i for i, v in enumerate(file_content) if input_end_str in v][0]

    input_lines = file_content[start_index:end_index]

    deps = [re.findall(r'\"(.+?)\"', x) for x in input_lines]

    deps = [x for x in deps if x not in [[], ['null'], ['__file__']]]

    return flatten(deps)


def make_target(fn,
                input_start_str = '# *** bubble input start ***',
                input_end_str = '# *** bubble input end ***'):

    deps = get_bubble_template_dependencies(fn, input_start_str, input_end_str)

    target_name = fn.split('.')[0].split('/')[-1]

    depends = deps[:-1]

    target = deps[-1]

    depends = '\\ \n\t'.join(depends)

    short_target = '\n' + target_name + ': ' + target + '\n\n'

    target = target + ': ' + fn + ' \\ ' + '\n' + '\t' + depends + '\n'

    return {'name': target_name, 'content': short_target + target}


def update_makefile(new_targets: list,
                    root: str = os.getcwd(),
                    target_start_str: str = '# *** bubble target start ***'):

    # add option to delete an existing target
    if not os.path.exists(root + '/Makefile'):

        raise FileNotFoundError('No Makefile found in current directory.')

    with open('Makefile') as m:

        makefile_lines = m.readlines()

    target_index = [i for i, x in enumerate(makefile_lines) if target_start_str in x][0]

    print(target_index)

    makefile_content = makefile_lines[:(target_index + 1)]

    new_targets_content = [x['content'] for x in new_targets]

    makefile_content = ''.join(makefile_content) + ''.join(new_targets_content)

    with open('Makefile', 'w') as m:

        m.write(makefile_content)

    print('Successfully updated %i Makefile targets. %s' % (len(new_targets), random_success()))
