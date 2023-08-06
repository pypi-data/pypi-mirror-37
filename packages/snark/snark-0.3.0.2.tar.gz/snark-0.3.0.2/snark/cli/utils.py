import snark
import pkg_resources
from outdated import check_outdated, warn_if_outdated
from subprocess import call
import subprocess
import os
from snark.exceptions import SnarkException

def get_cli_version():
    return "1.0.0" #TODO

def verify_cli_version():
    try:
        version = pkg_resources.get_distribution(snark.__name__).version
        is_outdated, latest_version = check_outdated(snark.__name__, version)
        if is_outdated:
            print('\033[93m'+"Snark is out of date. Please upgrade the package by running `pip3 install --upgrade snark`"+'\033[0m')
    except:
        pass

def check_program_exists(command):
    try:
        subprocess.call([command])
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
        else:
            # Something else went wrong while trying to run `wget`
            return True
    return True

def get_proxy_command(proxy):
    ssh_proxy = ""
    if proxy and proxy != " " and proxy != "None" and proxy != "":
        if check_program_exists('ncat'):
            ssh_proxy = '-o "ProxyCommand=ncat --proxy-type socks5 --proxy {} %h %p"'.format(proxy)
        else:
            raise SnarkException(message="This pod is behind the firewall. You need one more thing. Please install nmap by running `sudo apt-get install nmap` on Ubuntu or `brew install nmap` for Mac")
    return ssh_proxy
