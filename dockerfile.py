import os
from utils import scaffold, random_success


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
