# Repository Mirror Manager

Simple setup to manage RPM repository mirrors to save time and bandwidth working locally with VMs and containers. 

Repositories:

* CentOS 6.5 i386/x86_64 base and updates.
* CentOS 6 i386/x86_64 base and updates, EPEL, and Puppet Labs.
* CentOS 7 x86_64 base, updates, extras, and EPEL.

## Use

1. Identify path on host where mirrors will be saved.
2. Copy `example.config.rb` to `config.rb`, edit and add a shared folder for the mirror path mapping to */MIRRORS*.
3. Copy `example.mirrors.json` to `mirrors.json`, edit and add/update the *distro_list* and any other applicable settings.
4. Add repository-specific configurations in `repos.d/...`. These are the same as the files in `/etc/yum.repos.d/`. Note, use explicit architecture in the URLs (e.g. i386, x86_64, etc.).
5. Start the VM using `vagrant up`
6. Run the mirror script using `vagrant ssh -c ./run.sh`

## Configuration

### config.rb

There are settings to customize the VM (cpus, memory, gui, etc.) Additionally, there are settings for share folders. There needs to be at least one shared folder mapping to */MIRRORS* or whatever path is used in mirrors.json (*mirror_path*).

Example:

```
LocalConf.shared_folders = { './repo_mirrors' => '/MIRRORS' }
```

### mirrors.json

1. *mirror_path*\*, path where repository mirrors should be created. This corresponds to the shared directory in *config.rb*. Default is: "/MIRRORS".
2. *repo_conf_path*\*, path where repository configurations are maintained. Default is: "repos.d".
3. *distro_conf_path*\*, path where generated distro configurations are placed. Default is: "conf.d".
4. *script_path*\*, path where generated individual repository update scripts are placed. Default is: "scripts.d".
4. *log_path*\*, path where logs will be created. Default is: "logs".
5. *distro_list*, list of distributions to mirror:
    6. *name*, distro name (e.g. "CentOS", "Fedora", "RHEL")
    7. *description*, since comments are not allowed in json.
    8. *enabled*, is this distro enabled, should it be mirrored.
    9. *version*, distro version to mirror (e.g. "6", "7" or if using centos vault, "6.5", "7.0.1403", etc.)
    10. *arch_list*, list of architectures to mirror. (e.g. "i386", "x86_64")

\* If path is not absolute, it will be treated as relative to where the generator script resides.
