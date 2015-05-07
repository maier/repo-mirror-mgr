# -*- mode: ruby -*-
# vi: set ft=ruby :

# rubocop:disable Metrics/LineLength
# rubocop:disable Style/GlobalVars

# Customize VMs
# LocalConf.vm_gui = false
# LocalConf.vm_memory = 1024
# LocalConf.vm_cpus = 1

# Share additional folders, for example:
# LocalConf.shared_folders = {'/path/on/host' => '/path/on/guest', '/home/foo/app' => '/app'}
# or, to map host folders to guest folders of the same name,
# LocalConf.shared_folders = Hash[*['/home/foo/app1', '/home/foo/app2'].map{|d| [d, d]}.flatten]
#
# Note, the default mirror location is 'MIRRORS', if changed update here and in mirrors.json
#
# LocalConf.shared_folders = {'.' => '/MIRRORS'}
