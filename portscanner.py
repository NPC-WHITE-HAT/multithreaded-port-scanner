import socket
import threading
from rich.table import Table
from rich.console import Console
from rich.live import Live

console = Console()

# Create table
table = Table(title="[red]Port Scanner Results[/red]",style="purple")
table.add_column("Port", justify="center", style="yellow")
table.add_column("Status", justify="center", style="green") 

# List to store open ports
open_ports = []

# Scan function
def scan_port(target_ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((target_ip, port))

    if result == 0:
        open_ports.append(port)

    s.close()

# Input target
target = input("Enter your target: ")

try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    console.print("[red]Invalid hostname or no internet[/red]")
    exit()

console.print(f"\n[bold yellow]Scanning {target_ip}...[/bold yellow]\n")

threads = []

# Live table display
with Live(table, refresh_per_second=4, console=console):

    for port in range(1, 1025):
        t = threading.Thread(target=scan_port, args=(target_ip, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Add results to table
    for port in sorted(open_ports):
        table.add_row(str(port), "OPEN")

console.print("\n[bold blue]Scan Completed[/bold blue]")