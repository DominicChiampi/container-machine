import os
from dotenv import load_dotenv
from fabric import Connection
from invoke.exceptions import UnexpectedExit

load_dotenv("infra.env")
HOST = os.environ.get('HOST')
REMOTE_USER = os.environ.get('REMOTE_USER')
KEYFILE = os.environ.get('KEYFILE')
VERSION = os.environ.get('UBUNTU_VER')
PACKAGES = os.environ.get('PACKAGES').split(' ')

# Connect to the remote server
c = Connection(HOST, user=REMOTE_USER, connect_kwargs={"key_filename": KEYFILE})

def upgrade_ubuntu():
    """
    Upgrade the Ubuntu OS
    """
    c.sudo("sed -i 's/Prompt=lts/Prompt=normal/g' /etc/update-manager/release-upgrades")
    c.sudo('apt update')
    c.sudo('apt upgrade -y')
    c.sudo('apt dist-upgrade -y')
    c.sudo('apt autoremove -y')

def install_package(package):
    """
    Install the given package
    """
    c.sudo(f'apt install -y {package}')

def ubuntu_version_is(version):
    """
    Check if the Ubuntu version is less than the given version
    """
    try:
        c.sudo(f'lsb_release -sr | grep -c {version}')
    except UnexpectedExit:
        return False
    return True

def package_installed(package):
    """
    Check if the given package is installed
    """
    try:
        c.sudo(f'apt list --installed | grep -c {package}')
    except UnexpectedExit:
        return False
    return True

if __name__ == "__main__":
    if not ubuntu_version_is(VERSION):
        upgrade_ubuntu()

    # Install the packages
    for package in PACKAGES:
        install_package(package)
