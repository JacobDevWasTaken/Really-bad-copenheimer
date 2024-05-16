import time

import mcstatus
from concurrent.futures import ThreadPoolExecutor
import threading

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

to_add_ips: list = []
to_add_ports: list = []


def _scan(ip, port, logger):
    print("scanning")
    srv = mcstatus.JavaServer(host=ip, port=port)
    srv.status()
    logger(ip, port)


def _thread(logger):
    with ThreadPoolExecutor(max_workers=src.configloader.load_discover_config("Serverscanner.Threads")) as pool:
        while True:
            pool.map(_scan, to_add_ips, to_add_ports, [logger] * len(to_add_ips))
            time.sleep(0.1)


def start(logger):
    threading.Thread(target=_thread, args=(logger,)).start()


def add(ip, port):
    to_add_ips.append(ip)
    to_add_ports.append(port)
