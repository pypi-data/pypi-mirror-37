import os
import subprocess

from fabric.api import cd, env, run, prefix, local, lcd

"""
fab -H localhost local_freeze:version=0.1.20

"""


def freeze(user=None):
    env.user = user
    env.app_folder = f'/home/{env.user}/app'
    env.activate = 'source ~/.venvs/ambition/bin/activate'
    env.local_app_folder = '~/source/ambition-edc'
    with prefix(env.activate):
        with cd(env.app_folder):
            _pip_freeze()


def _pip_freeze():
    env.edc_version = run('git describe --abbrev=0 --tags')
    run(
        f'pip freeze | grep ambition > ~/freeze.{env.host}.v{env.edc_version}.txt && '
        f'pip freeze | grep edc- >> ~/freeze.{env.host}.v{env.edc_version}.txt')
    local(f'scp {env.user}@{env.host}:~/freeze.{env.host}.v{env.edc_version}.txt .')


def local_freeze(version=None, next_version=None):
    env.app_folder = '~/source/ambition-edc'
    env.activate = 'source ~/.venvs/ambition-edc/bin/activate'
    venv_folder = '~/.venvs/ambition-edc'
    file = f'{env.app_folder}/requirements/stable-v{version or next_version}.txt'
    local(f'rm -rf {venv_folder}')
    local(f'python3 -m venv {venv_folder}')
    with prefix(env.activate):
        with lcd(env.app_folder):
            local('git checkout master')
            if version:
                v = local('git describe --abbrev=0 --tags', capture=True)
                assert v == version, f'non-matching version numbers. You gave {version}. Got last tag is {v}'
            local('pip install -U pip ipython --no-cache-dir')
            local('pip install -U -r requirements/stable.txt --no-cache-dir')
            local(f'pip freeze | grep ambition > {file} && '
                  f'pip freeze | grep edc- >> {file}')
            local('git checkout develop')


def diff_freeze(version):
    app_folder = '~/source/ambition-edc'
    report_file = f'{app_folder}/freeze_diff.txt'
    local(f'echo "{version}" > {report_file}')
    with open(os.path.expanduser(
            '~/source/ambition-edc/fabfile/.hosts'), 'r') as f:
        hosts = f.readlines()
    for host in hosts:
        host = host.strip()
        #         local(
        # f'echo "{app_folder}/freeze.{host}.v{version}.txt" >> {report_file}')
        command = (
            f'diff -y {app_folder}/freeze.{host}.v{version}.txt '
            f'{app_folder}/requirements/stable-v{version}.txt')
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        output, _ = process.communicate()
        print(output)
        # local(f'echo "{output}" >> {report_file}')
    local(f'cat {report_file}')
