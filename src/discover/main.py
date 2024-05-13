import threading

import src.configloader

import src.discover.port_scanner.workerSimple
import src.discover.port_scanner.workerAsyncio
import src.discover.port_scanner.workerNonBlockingSockets

GREEN = "\033[1;32;48m"
YELLOW = "\033[1;33;48m"
RED = "\033[1;31;48m"
END = "\033[1;37;0m"

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

def main():
    port_scanner_mode = src.configloader.load_discover_config("Portscanner.Mode")

    def logger(ip, port):
        print("Found open port: " + ip + ":" + str(port))

    func = None

    if port_scanner_mode == "SimpleThreaded":
        pass

    elif port_scanner_mode == "AsyncioBatchThreaded":
        func = src.discover.port_scanner.workerAsyncio.run_worker

    elif port_scanner_mode == "NonBlockingSocketsThreaded":
        func = src.discover.port_scanner.workerNonBlockingSockets.run_worker

    if func:
        for i in range(src.configloader.load_discover_config("Portscanner.Threads")):
            th_ = threading.Thread(target=func, args=(logger,))
            th_.start()
