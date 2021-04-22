from fabric.contrib.files import append, exists, sed
from fabric.api import cd, env, local, run
import random

REPO_URL = 'https://github.com/pka69/Pan_Barnaba_New.git'
HOST = 'panbarnaba.pl' 
'''
git reset --hard
git pull

'''

def deploy():
    site_folder = '/home/elephant69/domains/{}/public_python/'.format(HOST)
    source_folder = '/home/elephant69/repo/{}/'.format(HOST)

    _create_directory_structure_if_neccessary(site_folder)
    _get_latest_source(source_folder_update_settings(source_folder, env.host))
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

def _create_directory_structure_if_neccessary(site_folder):
    for subfolder in ('app'):
        run('mkdir -p {}/{}'.format(site_folder, subfolder))

def _get_latest_source(source_folder):
    if exists(source_folder+'/.git'):
        run ('cd {} git fetch'.format(source_folder))
    else:
        run ('git clone {} {}'.format(REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd {} && git reset --hard {}'.format(source_folder, current_commit))

