#!/usr/bin/env bash

config_script="${HOME}/mirror/generate-mirror-configs.py"
[ -x $config_script ] || { echo "Configuration script not found ($config_script)."; exit 1; }
echo "Generating configurations and repository mirror update script."
$config_script
[ $? -eq 0 ] || { echo "Error running configuration script."; exit 1; }
echo

update_script="${HOME}/mirror/mirror.sh"
[ -x $update_script ] || { echo "Error, mirror update script ($update_script) not generated."; exit 1; }
echo "Updating repository mirrors:"
$update_script

# END
