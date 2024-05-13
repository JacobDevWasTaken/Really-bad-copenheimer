import socket
import struct
import json

def unpack_varint(s):
    d = 0
    for i in range(5):
        b = ord(s.recv(1))
        d |= (b & 0x7F) << 7*i
        if not b & 0x80:
            break
    return d

def pack_varint(d):
    o = b""
    while True:
        b = d & 0x7F
        d >>= 7
        o += struct.pack("B", b | (0x80 if d > 0 else 0))
        if d == 0:
            break
    return o

def pack_data(d):
    h = pack_varint(len(d))
    if type(d) == str:
        d = bytes(d, "utf-8")
    return h + d


def pack_port(i):
    return struct.pack('>H', i)


def get_cracked(host, proto_version, port=25565):


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # Send handshake
    s.send(pack_data(
        b"\x00" + #packet id
        pack_varint(proto_version) + #protocol version
        pack_data(host.encode('utf8')) + #ip
        pack_port(port) + #port
        b"\x02" #nextstate
        ))
    
    s.send(pack_data(
        b"\x00" + #packet id
        pack_data("notch".encode("utf8")) + #username
        b"\x00"*16 #uuid
        ))

    # Read response

    res = s.recv(1)

    s.close()

    if res == b"\x03":
        return "Cracked"
    elif res == b"\xab":
        return "Online"
    else:
        return "Unknown"
