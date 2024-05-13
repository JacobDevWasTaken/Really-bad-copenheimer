import os
import subprocess
import sys

import src.daemon.daemon
import src.interface.cli
import src.discover.main

VERSION = "v1.3.0"

if __name__ == "__main__":
    logo = f"""
     _____ ____  _____  ______ _   _ _    _ ______ _____ __  __ ______ _____  
    / ____/ __ \\|  __ \\|  ____| \\ | | |  | |  ____|_   _|  \\/  |  ____|  __ \\ 
   | |   | |  | | |__) | |__  |  \\| | |__| | |__    | | | \\  / | |__  | |__) |
   | |   | |  | |  ___/|  __| | . ` |  __  |  __|   | | | |\\/| |  __| |  _  / 
   | |___| |__| | |    | |____| |\\  | |  | | |____ _| |_| |  | | |____| | \\ \\ 
    \\_____\\____/|_|    |______|_| \\_|_|  |_|______|_____|_|  |_|______|_|  \\_\\
    
    Copenheimer {VERSION}
    https://github.com/JacobborstellCoder/Really-bad-copenheimer
    """

    if len(sys.argv) == 1:
        print(logo)
        print("Usage: [cli | start-daemon]")
        print("System commands (intended for use within the program):")
        print("[daemon-run | discover-run | rescan-run]")

    elif len(sys.argv) == 2:
        if sys.argv[1].lower() == "cli":
            print(logo)
            src.interface.cli.start()
        elif sys.argv[1].lower() == "daemon-run":
            src.daemon.daemon.start()
        elif sys.argv[1].lower() == "discover-run":
            src.discover.main.main()
        elif sys.argv[1].lower() == "rescan-run":
            pass
        elif sys.argv[1].lower() == "start-daemon":
            if os.name == "posix":
                cmd = "( " + sys.executable + " " + __file__ + " daemon-run & )"
                print(cmd)
                proc = subprocess.Popen(["/bin/zsh", "-c", cmd], stderr=subprocess.STDOUT)
