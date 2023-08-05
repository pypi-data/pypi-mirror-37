import os
import sys
import subprocess
import traceback
import glob

print('Using python: {prefix}'.format(prefix=sys.prefix))

tag_name = os.environ.get('TRAVIS_TAG', 'false')
token = os.environ.get('CONDA_TOKEN', 'NOT_A_TOKEN')
repo_branch = os.environ.get('TRAVIS_BRANCH', '')
is_pull_request = os.environ.get('TRAVIS_PULL_REQUEST', 'false')

if is_pull_request == 'false':
    is_pull_request = False
elif is_pull_request == 'true':
    is_pull_request = True
else:
    raise RuntimeError('{val} defined for "is_pull_request"'.format(name=val))

print("ENVIRONMENTAL VARIABLES:")
print("\t$TRAVIS_TAG = ", tag_name)
print("\t$TRAVIS_BRANCH = ", repo_branch)
print("\t$TRAVIS_PULL_REQUEST = ", is_pull_request)


if tag_name and tag_name.startswith('v'):
    print('Tag made for release:')
    print('Building for "main" channel......')
    _build = True
    channel = 'main'
    # os.environ['BUILD_STR'] = ''
elif repo_branch == 'master' and not is_pull_request:
    # if($env:APPVEYOR_REPO_BRANCH -eq "master" -and !$env:APPVEYOR_PULL_REQUEST_NUMBER)
    print('Commit made to master, and not PR:')
    print('Building for "dev" channel......')
    _build = True
    channel = 'dev'
    # os.environ['BUILD_STR'] = 'dev'
elif is_pull_request:
    print('Build is for a PR, not building.....')
    _build = False
else:
    _build = False

if _build:
    try:
        cmd = ' '.join(['conda', 'build', os.path.join('.ci', 'conda-recipe'),
                        '--output-folder', os.path.join('.ci', 'conda-build'),
                        '--no-test'])
        response = subprocess.check_output(cmd, shell=True)
        print('Build succeeded.')
    except subprocess.CalledProcessError:
        print('\n\nBuild failed.\n\n')
        traceback.print_exc()
else:
    print('No indicators made to build:')
    print('Not building.......')
