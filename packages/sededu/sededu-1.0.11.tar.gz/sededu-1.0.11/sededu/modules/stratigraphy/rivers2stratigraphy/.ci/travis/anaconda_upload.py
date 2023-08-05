import os
import sys
import subprocess
import traceback
import glob

print('Using python: {prefix}'.format(prefix=sys.prefix))

tag_name = os.environ.get('TRAVIS_TAG', '')
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
    print('Uploading for "main" channel......')
    _upload = True
    channel = 'main'
    # os.environ['BUILD_STR'] = ''
elif repo_branch == 'master' and not is_pull_request:
    # if($env:APPVEYOR_REPO_BRANCH -eq "master" -and !$env:APPVEYOR_PULL_REQUEST_NUMBER)
    print('Commit made to master, and not PR:')
    print('Uploading for "dev" channel......')
    _upload = True
    channel = 'dev'
    # os.environ['BUILD_STR'] = 'dev'
elif is_pull_request:
    print('Build is for a PR, not deploying.....')
    _upload = False
else:
    _upload = False

if _upload:
    # try to locate the built file, 
    # if you can't find it, assume build failed
  
    expected_path = os.path.join('.ci', 'conda-build', '**',
                                 'rivers2stratigraphy*bz2')
    binary_path = glob.glob(expected_path)
    binary_path = binary_path[0]
    if os.path.isfile(binary_path):
        print('File to upload located at:\n\t', binary_path)
    else:
        raise RuntimeError('{name}: not a file'.format(name=binary_path))

    cmd = ' '.join(['anaconda', '-t', token, 'upload', '--force',
                    '--user', 'sededu', '--channel', channel,
                    binary_path])

    try:
        subprocess.check_call(cmd, shell=True)
        print('Upload succeeded to {channel} for file:\n\t{file}'.format(channel=channel,file=binary_path))
    except subprocess.CalledProcessError:
        traceback.print_exc()
else:
    print('No indicators made to upload:')
    print('Not uploading.......')