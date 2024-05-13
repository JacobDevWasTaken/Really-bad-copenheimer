import socket
import selectors
import random
import ipaddress
import time

import src.configloader

"""
Really-Bad-Copenheimer
Copyright (C) <2024>  <Jacob Borstell>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

TIMEOUT = src.configloader.load_discover_config("Portscanner.TimeoutSeconds")
PORTS = src.configloader.load_discover_config("Portscanner.Ports")
BATCH_SIZE = src.configloader.load_discover_config("Portscanner.NonBlockingSocketsThreaded.BatchSize")

GREEN = "\033[1;32;48m"
YELLOW = "\033[1;33;48m"
RED = "\033[1;31;48m"
END = "\033[1;37;0m"

running = True

BAD_IPS = []
with open("src/discover/port_scanner/exclude.txt", "r") as file:
    for line in file:
        line = line.rstrip("\n")
        line = line.split(" ")[0]
        if len(line) == 0:
            continue
        if line[0] == "#":
            continue
        if "-" in line:
            start_ip, end_ip = line.split('-')
            start_ip, end_ip = ipaddress.IPv4Address(start_ip.strip()), ipaddress.IPv4Address(end_ip.strip())
            BAD_IPS.extend(list(ipaddress.summarize_address_range(start_ip, end_ip)))
        else:
            BAD_IPS.append(ipaddress.IPv4Network(line))


def is_bad_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        for ip_range in BAD_IPS:
            if ip_obj in ip_range:
                return True

    except Exception:
        return True

    return False


def _stop():
    global running
    running = False


def random_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"


def scan_batch(size: int, logger):
    pollObj = selectors.PollSelector()

    sockets = {}
    for i in range(size):
        ip = random_ip()
        if not is_bad_ip(ip=ip):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(TIMEOUT)
            sock.setblocking(False)
            try:
                sock.connect(("127.0.0.1", 8000))
            except BlockingIOError:
                pass
            res = pollObj.register(sock, selectors.EVENT_WRITE)
            sockets[res] = (ip, sock)
            print("sockets size", len(sockets))



    while sockets:
        print("sockets size", len(sockets))

        events = pollObj.select()

        for key, mask in events:
            logger(sockets[key][0], 25250)
            sockets[key][1].close()
            del sockets[key]


def run_worker(logger):
    time.sleep(1)
    while running:
        print("Scanned batch")
        scan_batch(BATCH_SIZE, logger)
