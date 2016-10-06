# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  # Configuration for events server
  config.vm.define "events" do |events|

    # ubuntu flavor and hostname
    events.vm.box = "ubuntu/trusty64"
    events.vm.hostname = 'events'
    events.vm.box_url = "ubuntu/trusty64"

    # set portforwarding
    events.vm.network :forwarded_port, guest: 80, host: 4567

    # set agent forwarding
    events.ssh.forward_agent = true

    # set box specs
    events.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--memory", 512]
      v.customize ["modifyvm", :id, "--name", "events"]
    end

    # Sync local files to virtual machine
    config.vm.synced_folder '.', '/www/normalize_events', owner: 'www-data', group: 'www-data', mount_options: ['dmode=755,fmode=755']

    # set ansible verbosity and run playbook
    events.vm.provision "ansible" do |ansible|
      # ansible.verbose = "vvv"
      ansible.playbook = "tasks/local.yml"
    end
    
  end
  
end
