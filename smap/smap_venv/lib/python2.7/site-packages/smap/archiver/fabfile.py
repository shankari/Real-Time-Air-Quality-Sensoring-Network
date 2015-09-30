# -*- python -*-

import os
import time
from fabric.api import run, env, task
from fabric.context_managers import cd, prefix

env.hosts = ['smap@local.cs.berkeley.edu']
env.password = '410soda'
env.roledefs['archivers'] = ['local', 'smote']
env.roledefs['smapsvcs'] = ['local']
env.forward_agent = True

env.deploy_path = '/project/eecs/tinyos/corytestbed/local/deploy'
env.prefix = '/project/eecs/tinyos/corytestbed/local/'

env.readingdb_repo = 'git@github.com:stevedh/readingdb.git'
# env.smap_repo = 'svn+ssh://stevedh@smote.cs.berkeley.edu/code/smap/branches/v2'
env.smap_repo = 'https://smap-data.googlecode.com/svn/trunk'

env.build_env = {
    'LD_LIBRARY_PATH': '/project/eecs/tinyos/corytestbed/local/lib/',
    'CFLAGS': '-I/project/eecs/tinyos/corytestbed/local/include/',
    'LDFLAGS': '-L/project/eecs/tinyos/corytestbed/local/lib/',
    'PYTHONPATH': '/project/eecs/tinyos/corytestbed/local/lib/python2.6/site-packages:/project/eecs/tinyos/corytestbed/local/usr/local/lib/python2.6/dist-packages',
    'PATH': '/usr/local/bin:/usr/mill/bin:/usr/pbs/bin:/usr/bin:/bin:/usr/bin/X11:/usr/sww/bin:/project/eecs/tinyos/corytestbed/local/bin'
}

env.run_env = {
    'LD_LIBRARY_PATH': '/project/eecs/tinyos/corytestbed/local/lib/',
}

def make_export(e):
    return 'export ' + ' '.join(map(lambda (k, v): k+'="'+v.replace(r'"', r'\"') + '"', 
                                    e.iteritems()))

def ts():
    return time.strftime("%Y-%m-%dT%H:%m:%S")

@task
def push():
    this_push = os.path.join(env.deploy_path, env.host, ts())
    run('mkdir -p ' + this_push)
    with cd(this_push):
        run('git clone ' + env.readingdb_repo)
        run('svn co ' + env.smap_repo + ' smap-data')
    ln = os.path.join(env.deploy_path, env.host, 'current')
    run('rm -f ' + ln)
    run('ln -s ' + this_push + ' ' + ln)

@task
def build():
    with prefix(make_export(env.build_env)):
        with cd(os.path.join(env.deploy_path, env.host, 'current', 'readingdb')):
            run('autoreconf --install')
            run('./configure')
            run('make')
        with cd(os.path.join(env.deploy_path, env.host, 'current', 'smap-data', 'python')):
            run('python setup.py build')

# @task
# def install():
#     monitize = os.path.join(env.deploy_path, env.host, 'current', 'smap-data', 'bin', 'smap-monitize')
#     run_env = env.run_env
#     run_env['PYTHONPATH'] = os.path.join(env.deploy_path, env.host, 'current', 'smap-data', 'python') + ':' + \
#         os.path.join(env.deploy_path, env.host, 'current', 'readingdb', 'iface_bin') + ':' + env.build_env['PYTHONPATH']
#     run_env['PATH'] = env.build_env['PATH']

    
#     with prefix(make_export(run_env)):
#         run(monitize + '-v ' + os.path.join(env.prefix, 'var', 'smap2') + \
#                 '-s ' + os.path.join(env.prefix, 'etc', 'smap') + \
#                 '-m ' + os.path.join(env.prefix, 'etc', 'monit.d')

@task
def restart():
    run("monit restart archiver")

@task
def deploy():
    run('ls')
