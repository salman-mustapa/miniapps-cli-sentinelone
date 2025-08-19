import sys
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import api  # Import modul API yang kita buat

# Import modul config buatan kita
import config

console = Console()

#fungsi untuk menampilkan menu utama
def show_menu():
    console.print("\n[bold cyan]SentinelOne CLI Tools[/bold cyan]")
    console.print("1. List Agent")
    console.print("2. Detailt Agent")
    console.print("3. Detail user")
    console.print("4. Generate Report")
    console.print("5. Exit")

# Dummy function untk list agent (sementara belum ke API asli)
def list_agents(cfg):
    try:
        agents = api.get_agents(cfg["base_url"], cfg["api_token"])

        table = Table(title="List Agent")
        table.add_column("Endpoint Name", style="yellow", no_wrap=True)
        table.add_column("OS", no_wrap=True)
        table.add_column("Mitigation Malecious", style="red", no_wrap=True)
        table.add_column("Mitigation Suspicious", style="red", no_wrap=True)
        table.add_column("Network Status", style="green", no_wrap=True)
        table.add_column("IP Address", style="yellow", no_wrap=True)
        table.add_column("Last Report IP", style="yellow", no_wrap=True)
        table.add_column("Status", style="green", no_wrap=True)

    # Data dummy (nanti kita ganti dengan API call)
    # agents = [
    #     {"id": "001", "endpointName": "SERVER A", "osType": "Windows", "status": "Active"},
    #     {"id": "002", "endpointName": "Agent B", "osType": "Linux", "status": "Inactive"},
    #     {"id": "003", "endpointName": "Agent C", "osType": "Windows", "status": "Active"}
    # ]

    # for agent in agents:
    #     table.add_row(agent["id"], agent["endpointName"], agent["osType"], agent["status"])

    #use API
        for agent in agents:
            # Ambil semua interfaces
            interfaces = agent.get("networkInterfaces", [])
            #Kumpulkan semua IPV4 dari semua interface
            ipv4_list = []
            for iface in interfaces:
                ipv4_list.extend(iface.get("inet", []))

            # Gabungkan jadi string, kalau kosong kasih tanda "-"
            ip_address = ", ".join(ipv4_list) if ipv4_list else "-"

            table.add_row(
                agent.get("computerName", "-"),
                agent.get("osName", "-"),
                agent.get("mitigationMode", "-"),
                agent.get("mitigationModeSuspicious", "-"),
                agent.get("networkStatus", "-"),
                ip_address,
                agent.get("lastIpToMgmt", "-"),
                "Active" if agent.get("isActive", False) else "Inactive"
            )

        console.print(table)  
    except Exception as e:
        console.print(f"[red]Error Load Data: {e}[/red]")  


# Main function
def main():
    # load config
    cfg = config.load_config()
    if not cfg:
        console.print("[yellow]File config tidak ditemukan. [/yellow]")
        base_url = Prompt.ask("Masukkan Base URL")
        api_token = Prompt.ask("Masukkan API Token")
        config.save_config(base_url, api_token)
        console.print("[green]Config telah disimpan![/green]")
        cfg = {"base_url": base_url, "api_token": api_token}

    while True:
        show_menu()
        choice = Prompt.ask("Pilih menu")

        if choice == "1":
            list_agents(cfg)
        elif choice == "2":
            console.print("[blue]Detail Agent belum tersedia.[/blue]")
        elif choice == "3":
            console.print("[blue]Detail User belum tersedia.[/blue]")
        elif choice == "4":
            console.print("[blue]Generate Report belum tersedia.[/blue]")
        elif choice == "5":
            console.print("[bold red]Exiting...[/bold red]")
            sys.exit(0)
        else:
            console.print("[red]Pilihan tidak valid. Silakan coba lagi.[/red]")

if __name__ == "__main__":
    main()