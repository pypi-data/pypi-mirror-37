import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(('0.0.0.0', 55555))
sock.sendto(b'Hello world', ('10.0.0.1', 55555))