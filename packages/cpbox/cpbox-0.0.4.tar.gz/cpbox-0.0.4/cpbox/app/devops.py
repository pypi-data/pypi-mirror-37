import sys
import commands
import subprocess
import socket
import os

from os import path
from cpbox.app.appconfig import appconfig
from cpbox.tool import utils
from cpbox.tool import file
from cpbox.tool import logger

class DevOpsApp:
    class Error(Exception):
        """
        DevOpsApp Error
        """
        pass

    def __init__(self, app_name, log_level='debug'):
        appconfig.init(app_name)
        syslog_ng_server = os.environ['PUPPY_SYSLOG_NG_SERVER'] if 'PUPPY_SYSLOG_NG_SERVER' in os.environ else None
        logger.make_logger(app_name, log_level, syslog_ng_server, True)
        self.logger = logger.getLogger(app_name)

        self.hostname = socket.gethostname()
        self.env = os.environ['PUPPY_ENV'] if 'PUPPY_ENV' in os.environ else 'dev'
        self.group_names = os.environ['PUPPY_GROUPS'].split(',') if 'PUPPY_GROUPS' in os.environ else []

        self.root_dir = path.dirname(path.realpath(sys.argv[0]))
        self.roles_dir = self.root_dir + '/roles'
        app_root_dir = self.roles_dir + '/' + app_name

        self.app_config_dir =  app_root_dir + '/config'
        self.app_templates_dir =  app_root_dir + '/templates'
        self.app_scripts_dir =  app_root_dir + '/scripts'

        self.app_storage_dir = '/opt/data/' + app_name
        self.app_persitent_storage_dir = self.app_storage_dir + '/persistent'
        self.app_runtime_storage_dir = self.app_storage_dir + '/runtime'
        self.app_logs_dir = self.app_runtime_storage_dir + '/logs'

        self._ensure_dir_and_write_permision()

        self.file_lock = None

    def run_cmd_ret(self, cmd):
        return self.run_cmd(cmd)[1]

    def run_cmd(self, cmd):
        self.logger.info('run_cmd: %s', cmd)
        ret = commands.getstatusoutput(cmd)
        return ret

    def shell_run(self, cmd):
        self.logger.info('shell_run: %s', cmd)
        return subprocess.call(cmd, shell=True)

    def _ensure_dir_and_write_permision(self):
        file.ensure_dir(self.app_storage_dir)
        file.ensure_dir(self.app_persitent_storage_dir)
        file.ensure_dir(self.app_runtime_storage_dir)
        file.ensure_dir(self.app_logs_dir)

    def _check_lock(self):
        filepath = self.app_runtime_storage_dir + '/locks/' + file.compute_lock_filepath(sys.argv)
        file_lock = file.obtain_lock(filepath)
        if file_lock is None:
            pid = 0
            with open(filepath, 'r') as f:
                pid = f.read()
            self.logger.warning('lock file exists, pid: %s => %s', pid, filepath)
            sys.exit(1)
        else:
            self.file_lock = file_lock
