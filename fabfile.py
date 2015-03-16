from contextlib import contextmanager
import json
import os
from timeit import reindent
from StringIO import StringIO
from fabric.api import *
from fabric.colors import green
from fabric.contrib.files import exists, contains

from fabtools import require
from fabtools.python import virtualenv as python_virtualenv


@task
def dev():
    env.host_string = '112.126.80.172'
    env.project_name = 'fitting'

    env.path = '/var/deploy/%s' % env.project_name
    env.activate = 'source ' + env.path + '/virt-python/bin/activate'

    env.depot = 'git@github.com:robinzhangx/Malicia-backend.git'
    env.depot_name = "fitting"
    env.branch = 'master'
    env.deployment_key = True

    env.mysql = False
    env.mysql_password = 'Fitting123'
    env.mysql_username = 'fitting'
    env.mysql_dbname = 'fitting'

    env.no_apt_update = True
    env.redis_port = 6379
    env.user = "lishuo"
    env.env_dict = {}

    env.static_dir = '/var/static/fitting'
    env.media_dir = '/var/media/fitting'
    env.wsgi_dir = '/var/wsgi/fitting'


def new_virtualenv():
    require.python.virtualenv(os.path.join(env.path, 'env'))


@contextmanager
def virtualenv():
    with python_virtualenv(os.path.join(env.path, 'env')):
        yield


@task
def install_nginx():
    with hide("output"):
        if not contains('/etc/apt/sources.list', 'nginx'):
            sudo('echo "deb http://ppa.launchpad.net/nginx/stable/ubuntu $(lsb_release -cs) main" >> /etc/apt/sources.list')
            sudo('apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C300EE8C')
            sudo("apt-get update")

        require.deb.package('nginx')
        put("vendor/nginx_util/*",  "/usr/bin/", use_sudo=True, mode="770")

@task
def init():
    """
    Setup the server for the first time
    :return:
    """

    banner("init")
    with show("output"):
        if not env.get('no_apt_update'):
            sudo('apt-get update')

        require.directory(env.path, mode="777", use_sudo=True)
        require.directory('/var/run/%s' % env.project_name, owner='www-data', group='www-data', mode='770', use_sudo=True)
        require.directory('/var/log/%s' % env.project_name, owner='www-data', group='www-data', mode='770', use_sudo=True)
        require.directory('/var/log/supervisord/', owner='www-data', group='www-data', mode='770', use_sudo=True)
        require.directory('/var/run/supervisord/', owner='www-data', group='www-data', mode='770', use_sudo=True)

        require.deb.packages([
            'gcc', 'python-all-dev', 'libpq-dev', 'libjpeg-dev', 'libxml2-dev', 'libxslt1-dev', 'libmysqlclient-dev',
            'libfreetype6-dev', 'libevent-dev', 'supervisor'
        ])
        require.python.pip(version="1.0")

        new_virtualenv()

        me = run('whoami')
        sudo('adduser %s www-data' % me)

        install_nginx()

        if env.mysql:
            require.mysql.server(password=env.mysql_password)
            with settings(mysql_user='root', mysql_password=env.mysql_password):
                require.mysql.user(env.mysql_username, env.mysql_password)
                require.mysql.database(env.mysql_dbname, owner=env.mysql_username)


@task
def check_out():
    banner("check out")
    require.git.command()

    if 'deployment_key' in env:
        run('mkdir -p ~/.ssh && chmod 700 ~/.ssh')
        put('deployment', '~/.ssh/id_rsa')
        run('chmod 600 ~/.ssh/id_rsa')

    with cd(env.path):
        if not exists(os.path.join(env.path, env.depot_name)):
            print green('Git folder not there, create it')
            run("git clone %s %s" % (env.depot, env.depot_name))
            sudo("chmod 777 %s" % env.depot_name)
            with cd(env.depot_name):
                run("git checkout %s" % env.branch)
        else:
            with cd(env.depot_name):
                with settings(warn_only=True):
                    run('git reset --hard HEAD')
                    run('git remote set-url origin %s' % env.depot)

                    result = run('git show-ref --verify --quiet refs/heads/%s' % env.branch)
                    if result.return_code > 0:
                        run('git fetch origin %s:%s' % (env.branch, env.branch))
                        run("git checkout %s" % env.branch)
                    else:
                        run('git checkout %s' % env.branch)
                        run('git pull origin %s' % env.branch)


@task
def config_webserver(is_quick=False):
    banner("config web server")
    with virtualenv():
        with cd(os.path.join(env.path, env.depot_name)):
            if not is_quick:
                run('pip install -r requirements.txt')

            with hide('output'):
                print green('Collect static files')

                run('python manage.py collectstatic --noinput')
                require.directory(env.static_dir, use_sudo=True)
                sudo('cp -r publish/* %s' % env.static_dir)
                sudo('rm -r publish')
                require.directory(env.media_dir, owner='www-data', group='www-data', mode='775', use_sudo=True)
                if exists(env.wsgi_dir):
                    sudo('rm -rf %s' % env.wsgi_dir + '.bak')
                    sudo('mv %s %s' % (env.wsgi_dir, env.wsgi_dir + '.bak'))
                require.directory(env.wsgi_dir, owner='www-data', group='www-data', mode='775', use_sudo=True)
                sudo('cp -r . %s' % env.wsgi_dir)
                sudo('chown -R www-data:www-data %s' % env.wsgi_dir)

            with cd(env.wsgi_dir):
                env.env_dict["environment"] = "prod"

                json_env = json.dumps(env.env_dict)
                put(StringIO(json_env), 'env.json', use_sudo=True)

                run("python manage.py migrate")

                put('config/supervisor/uwsgi.conf', '/etc/supervisor/conf.d/%s-uwsgi.conf' % env.project_name, use_sudo=True)
                sudo('supervisorctl -c /etc/supervisor/supervisord.conf update')
                sudo('supervisorctl -c /etc/supervisor/supervisord.conf restart uwsgi')

                put('config/nginx.conf', '/etc/nginx/sites-available/%s.conf' % env.project_name, use_sudo=True)
                with settings(warn_only=True):
                    sudo('rm /etc/nginx/sites-enabled/default')
                sudo('nginx_ensite %s.conf' % env.project_name)

            sudo('service nginx reload')


@task
def deploy():
    execute(init)
    execute(check_out)
    execute(config_webserver)
    banner('Deploy Succeeded. Go Home!')

@task
def quick_deploy():
    execute(check_out)
    execute(config_webserver, True)
    banner('Deploy Succeeded. Go Home!')


def banner(message):
    host_string = "%s (%s)" % (message, env.host_string)

    print green(reindent("""
    #########################################################################
    ## %s
    #########################################################################
    """ % host_string, 0))
