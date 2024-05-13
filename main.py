import os
import subprocess
import sys

import src.daemon.daemon
import src.interface.cli
import src.discover.main

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
