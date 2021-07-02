#!/usr/bin/env bash
#
# Install script for PALMS server
#
# Requirements:
#   The user on the remote host must have superuser privileges (to install the systemd service)
#   The remote host must already have RPi.GPIO installed (it can't be built cross-platform)
#
# To verify the status of the service, run "sudo systemctl status palms.service"
#

#### CONFIGURATION ####

REMOTE_USER="pi"
REMOTE_HOST="raspi"

#### END CONFIGURATION ####

REMOTE="${REMOTE_USER}@${REMOTE_HOST}"

my_echo() {
    echo
    echo "$@"
    echo
}

cd_script_dir() {
    cd "$(dirname "${BASH_SOURCE[0]}")"
}

copy_source() {
    my_echo "Copying PALMS source code to remote host"
    scp -r "$(pwd)/" "$REMOTE":~/server
}

install_server_pkg() {
    my_echo "Installing PALMS on remote host"
    ssh "$REMOTE" "
        cd ~/server/
        python3 -m pip install .
    "
}

install_systemd_service() {
    my_echo "Installing PALMS systemd service on remote host"
    ssh "$REMOTE" "
        cd ~/server/
        sudo mv ./palms.service /etc/systemd/system/palms.service
        sudo systemctl daemon-reload
        sudo systemctl start palms.service
    "
}

main() {
    cd_script_dir
    copy_source
    install_server_pkg
    install_systemd_service
}

main