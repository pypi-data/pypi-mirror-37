import os
import asyncio
import argparse

import uvloop

from fondue.protocol import main as protocol_main
from fondue.tap import Tap
from fondue.api import send_to_endpoint
from fondue.config import get_random_fondue_endpoint, write_config, read_config

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

loop = asyncio.get_event_loop()

parser = argparse.ArgumentParser('fondue')
parser.add_argument('-p', type=int, default=3333, help='The port to bind to', metavar='port', dest='port')
subparsers = parser.add_subparsers(dest='subcommand')
parser_serve = subparsers.add_parser('serve')
parser_install = subparsers.add_parser('install')
parser_view = subparsers.add_parser('view')
parser_add = subparsers.add_parser('add')
parser_add.add_argument('addr', type=str, help='The address of the peer to add', metavar='address')


def main():
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    if args.subcommand == 'serve':
        loop.run_until_complete(protocol_main(loop, parser, args))
    elif args.subcommand == 'install':
        # Get the id of the user that launched sudo
        user_id = int(os.environ.get('SUDO_UID', 0))
        username = os.environ.get('SUDO_USER', 'root')
        # Generate a new random VPN ip & MAC address
        vpn_ip, mac_addr = get_random_fondue_endpoint(as_string=True)
        # Create the tap device, and make it persistent
        # TODO: Does broadcast address/subnet mask need to be set
        tap = Tap(name='fond0', ip=vpn_ip, mac=mac_addr)
        tap.make_persistent(user_id)
        write_config({'vpn ip': vpn_ip, 'mac addr': mac_addr, 'interface': 'fond0'})
        print('Installed tap device %s at %s (%s) for user %s (%s)' % ('fond0', vpn_ip, mac_addr, username, user_id))
    else:
        loop.run_until_complete(send_to_endpoint(loop, args))

if __name__ == '__main__':
    main()
