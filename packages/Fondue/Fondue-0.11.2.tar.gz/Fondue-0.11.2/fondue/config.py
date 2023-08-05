import os
import random
import configparser
from socket import inet_ntoa

from fondue import ConfigError

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.fondue.settings')


def get_random_ip(subnet: int=10, as_string: bool=False):
    """ Get a random IPv4 address for the given subnet.

    Args:
        subnet (int): The class A subnet to choose from.
        as_string (bool): If True, return the address as a string. Otherwise return it as a bytes object.

    Returns: The IPv4 address.
    """
    tail = random.randint(1, 0xfffffe).to_bytes(3, 'big')
    bin_ip = bytes([subnet]) + tail
    if as_string:
        return inet_ntoa(bin_ip)
    else:
        return bin_ip


def get_random_fondue_endpoint(subnet: int=10, as_string: bool=False):
    """ Get a random IPv4 address and MAC address for the given subnet.

    Args:
        subnet (int): The class A subnet to choose from.
        as_string (bool): If True, return the address pairs as strings. Otherwise return them as bytes objects.

    Returns (tuple): The (IPv4 address, MAC address) tuple.

    """
    tail = random.randint(1, 0xfffffe).to_bytes(3, 'big')
    bin_ip = bytes([subnet]) + tail
    # MAC address is a locally administered, unicast address.
    # The first two bytes are fa:00,
    # The last four are the VPN ip.
    bin_mac = bytes([0xfa, 0, subnet]) + tail
    if as_string:
        return inet_ntoa(bin_ip), ':'.join('%02x' % b for b in bin_mac)
    else:
        return bin_ip, bin_mac


def write_config(data):
    config_parser = configparser.ConfigParser(data)
    with open(CONFIG_PATH, 'w') as f:
        config_parser.write(f)


def read_config():
    config_data = configparser.ConfigParser()
    if config_data.read(CONFIG_PATH) == 0:
        raise FileNotFoundError('Unable to load configuration data.')
    if any(s not in config_data['DEFAULT'] for s in ('vpn ip', 'interface', 'mac addr')):
        raise KeyError('Unable to load configuration data.')
    return config_data['DEFAULT']
