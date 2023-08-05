import socket
import platform
import os

from os import path
from cpbox.tool import template
import docker

def get_container(name):
    client = docker.from_env()
    container = None
    try:
        container = client.containers.get(name)
    except docker.errors.NotFound:
        pass
    return container

def remove_container(name, **kwargs):
    container = get_container(name)
    if container:
        container.remove(**kwargs)

def stop_container(name, **kwargs):
    container = get_container(name)
    if container:
        container.stop(**kwargs)

def get_os_name():
    os_name = platform.system()
    map = {
            'Linux': 'linux',
            'Darwin': 'mac',
            'CYGWIN': 'cygwin',
            'MINGW': 'MinGw',
            }
    for name, sys in map.iteritems():
        if os_name.startswith(name):
            return sys
    return 'unknown'

def base_docker_args(_env, _container_name, volumes=None, ports=None, current_user=False, envs=None, working_dir=None):
    _hostname = socket.gethostname()
    data = {
            '_env': _env,
            '_container_name': _container_name,
            '_hostname': _hostname,
            }

    args = '--name {{ _container_name }}'
    args += ' -h {{ _container_name }}.docker.{{ _hostname }}'
    args += ' -e PUPPY_ENV={{ _env }}'
    args += ' -e PUPPY_CONTAINER_NAME={{ _container_name }}'
    args += ' -e PUPPY_HOSTNAME={{ _hostname }}'

    if working_dir and os.path.isdir(working_dir):
        args += ' -w ' + working_dir

    if current_user:
        args += ' -u %s:%s' % (os.getuid(), os.getgid())

    if volumes:
        args += ' ' + ' '.join(('-v ' + from_ + ':' + to_ for from_, to_ in volumes.iteritems()))
    if ports:
        if isinstance(ports, dict):
            args += ' ' + ' '.join(('-p ' + str(from_) + ':' + str(to_) for from_, to_ in ports.iteritems()))
        else:
            args += ' ' + ' '.join(('-p ' + str(item) for item in ports))
    if envs:
        args += ' ' + ' '.join(('-e ' + item for item in envs))

    os_name = get_os_name()
    if os_name != 'mac':
        args += ' -v /etc/localtime:/etc/localtime'
    if path.isfile('/etc/devops'):
        args += ' -v /etc/devops/:/etc/devops/:ro'
    args = template.render_str(args, data)
    return args
