import asyncio
import ipaddress
import random
import time

import src.configloader

TIMEOUT = src.configloader.load_discover_config("Portscanner.TimeoutSeconds")
PORTS = src.configloader.load_discover_config("Portscanner.Ports")
BATCH_SIZE = src.configloader.load_discover_config("Portscanner.AsyncioBatchThreaded.BatchSize")

running = True

# Ips that you should probably not scan if you don't want legal trouble
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


async def scan_port(ip: str, port: int, logger):
    try:
        r, w = await asyncio.wait_for(asyncio.open_connection(host=ip, port=port), TIMEOUT)
        w.close()
        logger(ip, port)
    except Exception:
        pass


async def scan_batch(size, logger):
    tasks = []

    for i in range(round(size / len(PORTS))):
        scan_ip = random_ip()
        if is_bad_ip(scan_ip):
            continue

        for port in PORTS:
            tasks.append(scan_port(scan_ip, port, logger))

    await asyncio.gather(*tasks)


def run_worker(logger):
    time.sleep(1)
    while running:
        asyncio.run(scan_batch(BATCH_SIZE, logger))
