from rich.console import Console
from rich.table import Table
import api

console = Console()

def list_agents(cfg):
    """
    Fungsi untuk menampilkan list agent dari SentinelOne API
    Args:
        cfg (dict): dictionary berisi base_url dan api_token
    """
    try:
        # Inisialisasi 
        agents = api.get_agents(cfg["base_url"], cfg["api_token"])
        table = Table(title="List Agents")
        table.add_column("Endpoint Name", style="yellow")
        table.add_column("OS", style="magenta")
        table.add_column("Status", style="green")
        table.add_column("IP Address", style="cyan")

        for agent in agents:
            ipv4_list = []
            for iface in agent.get("networkInterfaces", []):
                ipv4_list.extend(iface.get("inet", []))
            ip_addr = ", ".join(ipv4_list) if ipv4_list else "-"

            table.add_row(
                agent.get("computerName", "-"),
                agent.get("osName", "-"),
                "Active" if agent.get("isActive", False) else "Inactive",
                ip_addr
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error Load Data: {e}[/red]")