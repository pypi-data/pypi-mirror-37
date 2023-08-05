import asyncio
import random
import socket
import uvloop


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class StunError(Exception):
    """ Raised when an error occurs during network discovery """


# Stun message types
BIND_REQUEST_MSG = b'\x00\x01'
BIND_RESPONSE_MSG = b'\x01\x01'
MAGIC_COOKIE = b'\x21\x12\xA4\x42'

# Stun attributes
MAPPED_ADDRESS = b'\x00\x01'
RESPONSE_ADDRESS = b'\x00\x02'
CHANGE_REQUEST = b'\x00\x03'
SOURCE_ADDRESS = b'\x00\x04'
CHANGED_ADDRESS = b'\x00\x05'
XOR_MAPPED_ADDRESS = b'\x00\x20'


# List of classic STUN servers
STUN_SERVERS = [('stun.ekiga.net', 3478), ('stun.ideasip.com', 3478), ('stun.voiparound.com', 3478),
                ('stun.voipbuster.com', 3478), ('stun.voipstunt.com', 3478), ('stun.voxgratia.org', 3478)]


class StunProtocol(asyncio.DatagramProtocol):
    def __init__(self, addr, loop, transport):
        self.addr = addr
        self.loop = loop
        self.transport = transport
        self.callback = None
        self.multiplexer = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        if self.callback:
            self.callback.set_result(data)

    def send_stun_message(self, msg_type, trans_id=None, data=b''):
        if trans_id is None:
            trans_id = random.getrandbits(128).to_bytes(16, 'big')
        msg_len = len(data).to_bytes(2, 'big')
        self.transport.sendto(msg_type+msg_len+trans_id+data, self.addr)
        return trans_id

    async def recv(self, timeout=60.0):
        self.callback = self.loop.create_future()
        try:
            result = await asyncio.wait_for(self.callback, timeout)
        finally:
            self.callback = None
        return result

    async def get_stun_response(self, trans_id=None, data=b'', max_timeouts=6):
        response = None
        timeouts = 0
        while timeouts < max_timeouts:
            try:
                trans_id = self.send_stun_message(BIND_REQUEST_MSG, trans_id, data)
                recv = await self.recv(timeout=0.5)
            except asyncio.TimeoutError:
                timeouts += 1
                continue
            if len(recv) < 20:
                continue
            msg_type, recv_trans_id, attrs = recv[:2], recv[4:20], recv[20:]
            msg_len = int.from_bytes(recv[2:4], 'big')
            if msg_len != len(attrs):
                continue
            if msg_type != BIND_RESPONSE_MSG:
                continue
            if recv_trans_id != trans_id:
                continue
            response = {}
            i = 0
            while i < msg_len:
                attr_type, attr_length = attrs[i:i+2], int.from_bytes(attrs[i+2:i+4], 'big')
                attr_value = attrs[i+4:i+4+attr_length]
                i += 4 + attr_length
                if attr_length % 4 != 0:  # If not on a 32-bit boundary, add padding bytes
                    i += 4 - (attr_length % 4)
                if attr_type in (MAPPED_ADDRESS, SOURCE_ADDRESS, CHANGED_ADDRESS):
                    family, port = attr_value[1], int.from_bytes(attr_value[2:4], 'big')
                    ip = socket.inet_ntoa(attr_value[4:8])
                    if family == 0x01:  # IPv4
                        if attr_type == XOR_MAPPED_ADDRESS:
                            cookie_int = int.from_bytes(MAGIC_COOKIE, 'big')
                            port ^= cookie_int >> 16
                            ip = int.from_bytes(attr_value[4:8], 'big') ^ cookie_int
                            ip = socket.inet_ntoa(ip.to_bytes(4, 'big'))
                            response['xor_ip'], response['xor_port'] = ip, port
                        elif attr_type == MAPPED_ADDRESS:
                            response['ext_ip'], response['ext_port'] = ip, port
                        elif attr_type == SOURCE_ADDRESS:
                            response['src_ip'], response['src_port'] = ip, port
                        elif attr_type == CHANGED_ADDRESS:
                            response['change_ip'], response['change_port'] = ip, port
                    else:  # family == 0x02  # IPv6
                        pass
            # Prefer XORed IPs and ports when possible
            xor_ip, xor_port = response.get('xor_ip', None), response.get('xor_port', None)
            if xor_ip:
                response['ext_ip'] = xor_ip
            if xor_port:
                response['ext_port'] = xor_port
            break
        return response

    # Get a STUN binding response from a server, without any CHANGE_REQUEST flags
    async def stun_test_1(self):
        await self.get_stun_response()

    async def get_ip_info(self):
        random.shuffle(STUN_SERVERS)
        for stun_addr in STUN_SERVERS:
            # Get the IP address of the stun host
            ip = socket.gethostbyname(stun_addr[0])
            if self.multiplexer:
                self.multiplexer.udp_connections.pop(self.addr, None)
            self.addr = (ip, stun_addr[1])
            if self.multiplexer:
                self.multiplexer.udp_connections[self.addr] = self
            response = await self.get_stun_response()
            if response and 'ext_ip' in response and 'ext_port' in response:
                return response['ext_ip'], response['ext_port']
        return None, None


def get_internal_ip(query_addr=('8.8.8.8', 80)):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('8.8.8.8', 80))  # Query Google's DNS
    int_ip = sock.getsockname()[0]
    sock.close()
    return int_ip


async def main(loop):
    transport, proto = await loop.create_datagram_endpoint(lambda: StunProtocol(None, loop, None), ('0.0.0.0', 3334))
    print(await proto.get_ip_info())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
