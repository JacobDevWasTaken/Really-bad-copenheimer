import getchlib, getchlib.keynames

from datetime import datetime
import time

from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live

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


console = Console()

selected = 0

def make_layout() -> Layout:
    layout = Layout(name="ui")

    layout.split(
        Layout(name="top", size=4),
        Layout(name="main"),
        Layout(name="bottom", size=3)
    )

    return layout



class Top:
    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)

        row1 = Table.grid(expand=True)
        row1.add_column(justify="center")
        row1.add_row("Really bad copenheimer V1.0",)

        row2 = Table.grid(expand=True)
        row2.add_column(justify="left")
        l = ["Info", "Help", "Config", "Logs", "Actions", "Servers"]
        l[selected] = "[grey0 on green3]" + l[selected] + "[/]"
        row2.add_row(l[0] + "  " + l[1] + "  " + l[2] + " | " + l[3] + "  " + l[4] + "  " + l[5] + " | [Q]uit",)

        grid.add_row(row1)
        grid.add_row(row2)

        return Panel(grid, style="bright_white on grey11")


class Bottom:
    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)

        grid.add_column(justify="left", min_width=60)
        grid.add_column(justify="right")

        grid.add_row("[link=https://github.com/JacobborstellCoder/Really-bad-copenheimer]https://github.com/JacobborstellCoder/Really-bad-copenheimer[/link]", datetime.now().ctime(),)
        
        return Panel(grid, style="bright_white on grey11")


class Main:
    def __rich__(self) -> Panel:
        if selected == 0:
            grid = Table.grid(expand=True)

            grid.add_column(justify="center")

            VERSION = "hi"

            grid.add_row(f"""
     _____ ____  _____  ______ _   _ _    _ ______ _____ __  __ ______ _____  
    / ____/ __ \|  __ \|  ____| \ | | |  | |  ____|_   _|  \/  |  ____|  __ \ 
   | |   | |  | | |__) | |__  |  \| | |__| | |__    | | | \  / | |__  | |__) |
   | |   | |  | |  ___/|  __| | . ` |  __  |  __|   | | | |\/| |  __| |  _  / 
   | |___| |__| | |    | |____| |\  | |  | | |____ _| |_| |  | | |____| | \ \ 
    \_____\____/|_|    |______|_| \_|_|  |_|______|_____|_|  |_|______|_|  \_\\



    Copenheimer {VERSION}
    [link=https://github.com/JacobborstellCoder/Really-bad-copenheimer]https://github.com/JacobborstellCoder/Really-bad-copenheimer[/link]
                                                   
            """)
            
            return Panel(grid,  style="bright_white on grey11")
        
        elif selected == 1:
            grid = Table.grid(expand=True)

            grid.add_column(justify="left")

            grid.add_row(f"""
[bold]Copenheimer[/bold]
                         
Copenheimer is a bot that scans the internet for minecraft servers. It can also monitor existing servers and log data such as their player count over time. Copenheimer has 3 main modules:
The port scanner: Copenheimer has a built-in port scanner to scan for open ports. It can also use the masscan port scanner if it is installed on the system.
The server scanner: When copenheimer finds an open port, it will scan that port for minecraft servers.
The monitor: Copenheimer can regularly ping servers and track data like player counts over time.

All of these options can be enabled, disabled and configured in the config.json file. For more info, please visit the github page:
[link=https://github.com/JacobborstellCoder/Really-bad-copenheimer]https://github.com/JacobborstellCoder/Really-bad-copenheimer[/link]
            """)
            
            return Panel(grid,  style="bright_white on grey11", padding=(2, 7,))
        elif selected == 2:
            grid = Table.grid(expand=True)

            grid.add_column(justify="left")

            grid.add_row(f"""
[bold]Work in progress[/bold]
            """)
            
            return Panel(grid,  style="bright_white on grey11")
        elif selected == 3:
            grid = Table.grid(expand=True)

            grid.add_column(justify="left")

            grid.add_row(f"""
[bold]Work in progress[/bold]
            """)
            return Panel(grid,  style="bright_white on grey11")
        elif selected == 4:
            grid = Table.grid(expand=True)

            grid.add_column(justify="left")

            grid.add_row(f"""
[bold]Work in progress[/bold]
            """)
            return Panel(grid,  style="bright_white on grey11")
        
        elif selected == 5:
            grid = Table.grid(expand=True)

            grid.add_column(justify="left")

            grid.add_row(f"""
[bold]Work in progress[/bold]
            """)
            return Panel(grid,  style="bright_white on grey11")
        
        return "here we go again"




layout = make_layout()
layout["top"].update(Top())
layout["main"].update(Main())
layout["bottom"].update(Bottom())


with Live(layout, refresh_per_second=10, screen=True):
    while True:
        time.sleep(0.05)
        res = getchlib.getkey(False, 0.15)
        if res == getchlib.keynames.RIGHT:
            selected = (selected + 1) % 6
        elif res == getchlib.keynames.LEFT:
            selected = (selected - 1) % 6
        elif res.lower() == "q":
            break
