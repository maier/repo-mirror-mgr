from __future__ import print_function
import json
import os
import sys


class Config(object):
    """configuration encapsulation"""
    def __init__(self, config_file):
        super(Config, self).__init__()

        self.base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        # if not an absolute path, fixup config file specification
        if config_file[0:1] != '/':
            config_file = os.path.join(self.base_dir, config_file)

        if not os.path.isfile(config_file):
            print("ERROR: main configuration file missing {}".format(config_file))
            sys.exit(1)

        self.config_file = config_file

        if not os.path.isfile(self.config_file):
            print("ERROR: config file missing {}".format(self.config_file))
            sys.exit(1)

        try:
            f = open(self.config_file, 'r')
            self.config = json.load(f)
        except Exception, e:
            raise e

        self.mirror_dir = self.check_path(self.config.get('mirror_path', '/MIRRORS'), False)
        self.conf_dir = self.check_path(self.config.get('distro_conf_path', 'conf.d'), True)
        self.repo_dir = self.check_path(self.config.get('repo_conf_path', 'repos.d'), True)
        self.script_dir = self.check_path(self.config.get('script_path', 'scripts.d'), True)
        self.log_dir = self.check_path(self.config.get('log_path', 'logs'), True)
        self.distro_list = self.config.get('distro_list', [])

        self.run_script = self.config.get('run_script', 'mirror.sh')
        if self.run_script[0:1] != '/':
            self.run_script = os.path.join(self.base_dir, self.run_script)

    def show(self):
        lines = [
            '=' * 50,
            '-- Base Configuration --',
            'Config file       : {}'.format(self.config_file),
            'Mirror path       : {}'.format(self.mirror_dir),
            'Distro config path: {}'.format(self.conf_dir),
            'Repo config path  : {}'.format(self.repo_dir),
            'Script path       : {}'.format(self.script_dir),
            'Log path          : {}'.format(self.log_dir),
            'Run script        : {}'.format(self.run_script),
            'Distro list       :'
        ]

        for distro in self.distro_list:
            lines.append("\t{} v{} ({}) {} - {}".format(
                distro['name'],
                distro['version'],
                ','.join(distro['arch_list']),
                'Enabled' if distro['enabled'] else 'Disabled',
                distro['description']))
        lines.append('=' * 50)
        print("\n".join(lines))
        print("\n")

    def check_path(self, path, create=False):

        if path[0:1] != '/':
            path = os.path.join(self.base_dir, path)

        if os.path.exists(path):
            return path

        if create:
            os.makedirs(path)
            return path

        return None
