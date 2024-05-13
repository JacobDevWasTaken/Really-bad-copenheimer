import threading

import src.configloader

import src.discover.port_scanner.workerSimple
import src.discover.port_scanner.workerAsyncio
import src.discover.port_scanner.workerNonBlockingSockets

GREEN = "\033[1;32;48m"
YELLOW = "\033[1;33;48m"
RED = "\033[1;31;48m"
END = "\033[1;37;0m"


def main():
    port_scanner_mode = src.configloader.load_discover_config("Portscanner.Mode")

    def logger(ip, port):
        print("Found open port: " + ip + ":" + str(port))

    if port_scanner_mode == "SimpleThreaded":
        pass

    elif port_scanner_mode == "AsyncioBatchThreaded":
        src.discover.port_scanner.workerAsyncio.run_worker(logger)

    elif port_scanner_mode == "NonBlockingSocketsThreaded":
        src.discover.port_scanner.workerNonBlockingSockets.run_worker(logger)
