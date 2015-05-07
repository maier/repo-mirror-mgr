# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'fileutils'

Vagrant.require_version '>= 1.7.0'

CONFIG = File.join(File.dirname(__FILE__), 'config.rb')
# local, override-able configuration options
# note, this is all "here" so that the Vagrantfile does
# not fail if there is no 'config.rb'.
module LocalConf
  class << self
    attr_accessor :vm_gui, :vm_cpus, :vm_memory, :shared_folders
  end
end
# defaults
LocalConf.vm_gui = false
LocalConf.vm_cpus = 1
LocalConf.vm_memory = 1024
LocalConf.shared_folders = { '.' => '/MIRRORS' }
require CONFIG if File.exist?(CONFIG)

Vagrant.configure(2) do |config|
  config.vm.box = 'maier/centos-7.1.1503-x86_64'

  config.vm.provider 'virtualbox' do |vb|
    vb.gui = LocalConf.vm_gui
    vb.cpus = LocalConf.vm_cpus
    vb.memory = LocalConf.vm_memory
  end

  LocalConf.shared_folders.each do |(host_folder, guest_folder)|
    config.vm.synced_folder host_folder.to_s, guest_folder.to_s
  end

  config.vm.synced_folder '.', '/home/vagrant/mirror'

  config.vm.provision 'shell', inline: <<-SHELL
    yum clean all && yum makecache fast && yum -y update
    yum -y install \
      yum-utils \
      yum-preso \
      createrepo
  SHELL
end
