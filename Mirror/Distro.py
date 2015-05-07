from __future__ import print_function

import errno
import os
import stat
# import sys
# import yum


class Distro(object):
    """Encapsulation for distro to mirror"""
    def __init__(self, config, distro):
        super(Distro, self).__init__()
        self.config = config

        self.name = distro['name']
        self.version = distro['version']
        self.enabled = distro['enabled']
        self.arch_list = {}

        for arch in distro['arch_list']:
            base_name = '{}-{}-{}'.format(self.name.lower(), self.version, arch)
            self.arch_list[arch] = {}

            self.arch_list[arch]['conf_file'] = os.path.join(
                self.config.conf_dir,
                '{}.conf'.format(base_name))

            self.arch_list[arch]['script_file'] = os.path.join(
                self.config.script_dir,
                '{}.sh'.format(base_name))

            self.arch_list[arch]['log_file'] = os.path.join(
                self.config.log_dir,
                '{}.log'.format(base_name))

            self.arch_list[arch]['repo_conf_dir'] = self.check_path(
                os.path.join(
                    self.config.repo_dir,
                    self.version,
                    arch),
                False)

            self.arch_list[arch]['reposync_cache_dir'] = self.check_path(
                os.path.join(
                    self.config.mirror_dir,
                    'cache.reposync',
                    self.name.lower(),
                    self.version,
                    arch),
                True)

            self.arch_list[arch]['createrepo_cache_dir'] = self.check_path(
                os.path.join(
                    self.config.mirror_dir,
                    'cache.createrepo',
                    self.name.lower(),
                    self.version,
                    arch),
                True)

            self.arch_list[arch]['mirror_dir'] = self.check_path(
                os.path.join(
                    self.config.mirror_dir,
                    self.name.lower(),
                    self.version,
                    arch),
                True)

    def show(self):
        for arch in self.arch_list:
            print('Distro         : {} v{} {}'.format(self.name, self.version, arch))
            print('Enabled?       : {}'.format('Yes' if self.enabled else 'No'))
            print("Repo configs  R: {}".format(self.arch_list[arch]['repo_conf_dir']))
            print("Config file   D: {}".format(self.arch_list[arch]['conf_file']))
            print("Script file   D: {}".format(self.arch_list[arch]['script_file']))
            print("Log file      D: {}".format(self.arch_list[arch]['log_file']))
            print("Mirror path   D: {}".format(self.arch_list[arch]['mirror_dir']))
            print("CR cache path D: {}".format(self.arch_list[arch]['createrepo_cache_dir']))
            print("RS cache path D: {}".format(self.arch_list[arch]['reposync_cache_dir']))
            print("\n")

    def check_path(self, path, create=False):
        """verify if a path exists, create if possible, otherwise error"""

        if os.path.exists(path):
            return path

        if create:
            os.makedirs(path)
            return path
        else:
            raise OSError([errno.ENOENT, 'Error: required path not found.', path])

        return None

    def clean(self, arch):
        """clean up dynamic, generated files for distro"""

        arch_def = self.arch_list.get(arch, None)

        if arch_def:
            if os.path.isfile(arch_def['conf_file']):
                os.remove(arch_def['conf_file'])
            if os.path.isfile(arch_def['script_file']):
                os.remove(arch_def['script_file'])

    def generate_distro_config(self, arch):
        """Generate distro config file (like /etc/yum.conf)"""

        arch_def = self.arch_list.get(arch, None)

        if not arch_def:
            raise KeyError('Invalid architecture specified.')

        try:
            with open(arch_def['conf_file'], 'w') as cfg:
                print("# Generated file !!! DO NOT EDIT !!!\n", file=cfg)
                print('[main]', file=cfg)
                print('reposdir={}'.format(arch_def['repo_conf_dir']), file=cfg)
        except Exception, e:
            raise e

    def generate_mirror_script(self, arch):
        """Generate reposync and createrepo script"""

        arch_def = self.arch_list.get(arch, None)

        if not arch_def:
            raise KeyError('Invalid architecture specified.')

        update_command_list = [
            "\n# reposync for {} {} {}".format(self.name, self.version, arch)
        ]

        update_command = [
            '/usr/bin/reposync',
            '--delete',
            '--arch={}'.format('i686' if arch == 'i386' else arch),
            '--config={}'.format(arch_def['conf_file']),
            '--cachedir={}'.format(arch_def['reposync_cache_dir']),
            '--download_path={}'.format(arch_def['mirror_dir']),
            '| tee {}'.format(arch_def['log_file'])
        ]

        update_command_list.append(" \\\n\t".join(update_command))

        update_command_list.append("\n# createrepo for {} {} {}".format(self.name, self.version, arch))
        update_command_list.append(
            '{}/mirror-repo-update.sh {} {}'.format(
                self.config.base_dir,
                arch_def['mirror_dir'],
                arch_def['createrepo_cache_dir']))

        try:
            with open(arch_def['script_file'], 'w') as script:
                print('#!/usr/bin/env bash', file=script)
                print('# This file is automatically generated.', file=script)
                print('# !!! DO NOT EDIT !!!', file=script)
                print('set -exu', file=script)
                for cmd in update_command_list:
                    print(cmd, file=script)
            os.chmod(arch_def['script_file'], stat.S_IRWXU)
        except Exception, e:
            raise e
