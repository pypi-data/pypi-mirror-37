#cython: language_level=3, boundscheck=True
import sys
import asyncio
import traceback
import pickle
from socket import inet_ntoa, inet_aton
from base64 import urlsafe_b64encode, urlsafe_b64decode

from fondue import __version__, FondueError


# Encode an (ip, port) address into a base64 string
def encode_addr(addr):
    return str(urlsafe_b64encode(inet_aton(addr[0]) + addr[1].to_bytes(2, byteorder='big')), 'utf-8')


# Encode a base64 string into an (ip, port) address
def decode_addr(encoded):
    raw = urlsafe_b64decode(encoded)
    return inet_ntoa(raw[:4]), int.from_bytes(raw[4:6], 'big')


class FondueServer:
    def __init__(self, parser, proto):
        self.parser = parser
        self.proto = proto

    async def client_connected(self, r, w):
        try:
            z = (await r.read()).decode('utf-8')
            args = self.parser.parse_args(z.split())
            if args.subcommand == 'view':
                data = {'local_ip': self.proto.local_ip, 'int_addr': self.proto.int_addr,
                        'ext_addr': self.proto.ext_addr, 'vpn_map': self.proto.vpn_map}
                w.write(pickle.dumps(data))
                await w.drain()
            elif args.subcommand == 'add':
                encoded_addr = args.addr
                if ':' in encoded_addr:
                    ip, port = encoded_addr.split(':')
                    addr = (ip, int(port))
                else:
                    addr = decode_addr(encoded_addr)
                await self.proto.add_peer(addr)
                data = {'local_ip': self.proto.local_ip, 'int_addr': self.proto.int_addr,
                        'ext_addr': self.proto.ext_addr, 'vpn_map': self.proto.vpn_map}
                w.write(pickle.dumps(data))
                await w.drain()
        except Exception as e:
            data = {'exception': traceback.format_exc()}
            w.write(pickle.dumps(data))
            await w.drain()
        finally:
            w.close()


async def start_endpoint(loop, parser, args, proto):
    server_obj = FondueServer(parser, proto)
    server = await asyncio.start_server(server_obj.client_connected, 'localhost', args.port, backlog=1)
    print('Serving on localhost:%s' % args.port)
    return server


def print_pool_data(data):
    local_ip, int_addr, ext_addr, vpn_map = data['local_ip'], data['int_addr'], data['ext_addr'], data['vpn_map']
    if local_ip:
        local_ip = inet_ntoa(local_ip)
    print('\nFondue v%s Network Pool\n' % __version__)
    print('VPN: %s INTERNAL: %s:%s EXTERNAL %s:%s\n' % (local_ip, int_addr[0], int_addr[1], ext_addr[0], ext_addr[1]))
    if vpn_map:
        print('{:<21} {:<21}\n'.format('VPN', 'EXTERNAL'))
        for vpn_addr, ext_addr in vpn_map.items():
            vpn_addr = inet_ntoa(vpn_addr)
            ext_addr = ext_addr[0] + ':' + str(ext_addr[1])
            print('{:<21} {:<21}'.format(vpn_addr, ext_addr))


async def send_to_endpoint(loop, args):
    try:
        r, w = await asyncio.open_connection('localhost', args.port)
    except OSError:
        print('Unable to connect to the Fondue service.')
    else:
        w.write(' '.join(sys.argv[1:]).encode('utf-8'))
        w.write_eof()
        serialized = await r.read()
        data = pickle.loads(serialized)
        if 'exception' in data:
            print(data['exception'])
            w.close()
            return
        if args.subcommand == 'view':
            print_pool_data(data)
        elif args.subcommand == 'add':
            print_pool_data(data)
        w.close()
