""" Class for sockets specifically running the Fondue protocol. """
import sys
import socket
import select
import hmac
from time import sleep
from math import pi
from enum import IntEnum
from random import randint
from threading import Lock
from timeit import default_timer as timer

from nescient.crypto.chacha import ChaChaCrypter


HEADER = b'FOND'


class Packet(IntEnum):
    GETEXTIP = 0x57
    SENDEXTIP = 0x58
    PEER1 = 0x59
    PEER2 = 0x60
    PEER3 = 0x61
    KEEPALIVE = 0x61  # TODO: Change this
    DATA = 0x63
    EDATA = 0x64
    KEX = 0x65


class PacketError(Exception):  # TODO: FondueError
    pass


def make_packet(type, data):
    # TODO: Add CRC
    return HEADER + bytes([type]) + data


def parse_packet(data):
    if len(data) < 5:
        raise PacketError('Invalid packet length.')
    elif data[:4] != HEADER:
        raise PacketError('Invalid packet header.')
    elif data[4] not in [item.value for item in Packet]:
        raise PacketError('Invalid packet type.')
    elif data[4] == Packet.KEX and not 6 < len(data) <= 103:
        raise PacketError('Invalid kex packet.')
    elif data[4] == Packet.EDATA and len(data) < 4 + 1 + 32 + 12:
        return PacketError('Invalid encrypted packet.')
    else:
        return {'type': data[4], 'data': data[5:]}


class FondueSocket:
    MTU = 32 + 12 + 1500 + 8

    def __init__(self, addr, vpn_addr=None, promiscuous=False):
        self.addr, self.vpn_addr, self.promiscuous = addr, vpn_addr, promiscuous
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(addr)
        self.socket_lock = Lock()
        self.remote_nodes = {}
        self.vpn_ips = {}
        self.sessions = {}
        self.keepalives = {}

    def add(self, remote, vpn_ip=None, encrypted=True):
        self.remote_nodes[remote] = vpn_ip
        if vpn_ip:
            self.vpn_ips[vpn_ip] = remote
        self.sessions[remote] = None if encrypted else False

    def peer(self, peer_addr):
        # TODO: Add this
        pass

    def remove(self, remote):
        vpn_ip = self.remote_nodes.pop(remote, None)
        if vpn_ip:
            self.vpn_ips.pop(vpn_ip, None)
        self.keepalives.pop(remote, False)
        self.sessions.pop(remote, None)

    def keepalive(self, peer_addr, interval=5):
        self.keepalives[peer_addr] = True
        while self.keepalives.get(peer_addr, False):
            # Send a keepalive packet
            with self.socket_lock:
                self.sock.sendto(make_packet(Packet.KEEPALIVE, bytes()), peer_addr)
            sleep(interval)

    def kex(self, peer_addr, interval=0.2, timeout=3, receipts=3):
        # TODO: Kex secure against MITM
        # Using a Diffie-Hellman key exchange and the First Oakley Group (RFC 2409 6.1)
        p = 2**768 - 2**704 - 1 + 2**64 * (int(2**638*pi) + 149686)
        g = 2
        # Compute secret 768-bit integer a, and A to send to peer
        a = randint(0, 2**768-1)
        A = pow(g, a, p)
        # B will be the integer received from Bob
        B = None
        kex_receipts = 0
        start, last_read, last_written = timer(), timer(), None
        # Grab the lock on the socket to avoid keepalives from using it
        with self.socket_lock:
            # TODO: Better syncing
            while kex_receipts < receipts:
                readable, writable, error = select.select([self.sock], [self.sock], [self.sock])
                if self.sock in error:
                    print('An error occurred.')  # TODO: Handle this?
                if self.sock in readable:
                    data, addr = self.sock.recvfrom(1508)
                    # Only accept packets from the peer
                    if addr == peer_addr:
                        # Only accept valid Fondue packets
                        try:
                            packet = parse_packet(data)
                            assert(1 < len(packet['data']) <= 97)
                        except (PacketError, AssertionError):
                            pass
                        else:
                            last_read = timer()
                            # The peer has received our a; keep sending acknowledgement packets
                            if packet['data'][0] == 0x1:
                                print('Received kex receipt.')
                                kex_receipts += 1
                            else:
                                print('Received kex.')
                            # Grab B from peer and convert to an int
                            B = int.from_bytes(packet['data'][1:], byteorder='little')
                else:
                    # If we have not received anything from B, end the key exchange
                    if timer()-last_read > timeout:
                        if kex_receipts == 0:
                            raise Exception('Unable to complete key exchange.')  # TODO: Exception type
                        break
                if self.sock in writable:
                    now = timer()
                    # Only send at most once every interval seconds.
                    if last_written is None or now-last_written > interval:
                        flag = bytes([1 if B else 0])
                        print('Sent kex receipt' if B else 'Sent kex')
                        self.sock.sendto(make_packet(Packet.KEX, flag + A.to_bytes(96, 'little')), peer_addr)
                        last_written = now
            # Compute the shared secret s = B**a mod p, convert it to bytes and take only the first 256 bits
            key = pow(B, a, p).to_bytes(96, 'little')[:32]
            # Try to synchronize with the peer before releasing the lock
            now = timer()
            if now-start < timeout:
                sleep(timeout-(now-start))
        print('Done:', ''.join('%02x' % i for i in key))
        # Build a ChaChaCrypter, an initial outgoing nonce, zero the incoming nonce for this peer's session
        self.sessions[peer_addr] = [ChaChaCrypter(key), randint(0, 2**96-1), 0]

    def sendto(self, data, addr):
        # If sending to a VPN node, get the remote address
        remote = self.vpn_ips.get(addr, addr)
        # Only allow packets to addresses that are remote nodes when not in promiscuous mode
        if not self.promiscuous and remote not in self.remote_nodes:  # Drop the packet
            return 0
        # If encrypted mode is selected, and no session info is available, do a key exchange
        if self.sessions.get(remote, False) is None:
            self.kex(remote)
        # If a session exists for this remote, encrypt data
        if self.sessions.get(remote, False):
            crypter, nonce, _ = self.sessions[remote]
            crypter.chacha_encrypt(data, nonce)
            # Authenticate the data
            nonce_b = nonce.to_bytes(12, 'little')
            auth_tag = hmac.new(crypter.key, nonce_b + data, digestmod='sha256').digest()
            # Increment the outgoing nonce
            self.sessions[remote][1] = (self.sessions[remote][1] + 1) % 2**96
            # Prepend the auth tag and nonce to the data
            data = bytearray(data)
            data[:] = auth_tag + nonce_b + data  # 32 auth bytes & 12 nonce bytes
            print(self.sessions)
            packet_type = Packet.EDATA
        else:
            packet_type = Packet.DATA
        # Grab the socket lock
        with self.socket_lock:
            self.sock.sendto(make_packet(packet_type, data), remote)

    def recvfrom(self, buffer_mtu=1508, allowed_timeouts=1):
        timeouts = 0
        while True:
            try:
                with self.socket_lock:
                    data, addr = self.sock.recvfrom(self.MTU)
                print('Raw:', list(data))
            except socket.timeout:
                if timeouts >= allowed_timeouts:
                    raise
                timeouts += 1
            else:
                # If not in promiscuous mode, ignore packets from non remote nodes
                if not self.promiscuous and addr not in self.remote_nodes:
                    continue
                try:
                    packet = parse_packet(data)
                except PacketError:
                    continue
                else:
                    data = packet['data']
                    # If received encrypted data and session info exists for this node
                    print(packet['type'])
                    if packet['type'] == Packet.EDATA and self.sessions.get(addr, False):
                        auth_tag, nonce_b, data = data[:32], data[32:44], bytearray(data[44:])
                        crypter, _, nonce = self.sessions[addr]
                        # Compare the calculated and received auth tags
                        new_auth_tag = hmac.new(crypter.key, nonce_b + data, digestmod='sha256').digest()
                        if not hmac.compare_digest(auth_tag, new_auth_tag):
                            print('Authentication tags not equal.')
                            continue
                        # Ignore packets with nonces less than the last received nonce
                        new_nonce = int.from_bytes(nonce_b, 'little')
                        if new_nonce <= nonce:
                            print('Incorrect nonce.')
                            continue
                        self.sessions[addr][2] = new_nonce
                        crypter.chacha_decrypt(data, new_nonce)
                        print(self.sessions)
                        return data, addr
                    elif packet['type'] == Packet.DATA:
                        return bytearray(data[:buffer_mtu]), addr
                    elif packet['type'] == Packet.KEX:
                        if data[0] == 0 and (self.sessions.get(addr, False) is None):  # TODO: When to remake
                            self.kex(addr)


if __name__ == '__main__':
    port = int(sys.argv[1])
    peer_port = port + 1 if port == 43434 else port - 1
    print('Bound to 0.0.0.0:' + str(port), peer_port)
    sock = FondueSocket(('', port))
    peer_addr = ('127.0.0.1', peer_port)
    sock.add(peer_addr)
    words = ['hello', 'world', 'test', 'encrypt']
    while True:
        if port == 43434:
            input()
            for i in range(4):
                sock.sendto(bytes(words[i], 'utf-8'), peer_addr)
                print('Sent:', words[i])
                input()
        else:
            data, _ = sock.recvfrom()
            try:
                s = str(data, 'utf-8')
            except Exception:
                print(list(data))
            else:
                print(s)