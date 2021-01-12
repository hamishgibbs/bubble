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

    input_lines = file_content[(start_index + 1):end_index]

    deps = [re.findall(r'\"(.+?)\"', x) for x in input_lines]

    return flatten(deps)


def make_target(fn,
                input_start_str = '# *** bubble input start ***',
                input_end_str = '# *** bubble input end ***'):

    # add option to delete an existing target

    if not os.path.exists('Makefile'):

        raise FileNotFoundError('No Makefile found in current directory.')

    with open('Makefile') as m:

        makefile_lines = m.readlines()

    deps = get_bubble_template_dependencies(fn)

    target_name = fn.split('.')[0].split('/')[-1]

    depends = deps[1:-1]

    target = deps[-1]

    depends = '\\ \n\t'.join(depends)

    short_target = target_name + ': ' + target + '\n\n'

    target = target + fn + ' \\ ' + '\n' + '\t' + depends + '\n'

    # Append this target to the makefile
    makefile_lines.insert(len(makefile_lines), short_target + target)

    makefile_content = ''.join(makefile_lines)

    with open('Makefile', 'w') as m:

        m.write(makefile_content)

    print('Successfully updated Makefile target "%s". %s' % (target_name, random_success()))


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
