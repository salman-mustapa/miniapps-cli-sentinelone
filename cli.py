import sys
import api  # Import modul API yang kita buat
import locale
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from datetime import datetime
from babel.dates import format_datetime

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

            # Tambahkan baris ke tabel
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

def detail_user(cfg):
    try:
        # Ambil data user
        user = api.get_user_details(cfg["base_url"], cfg["api_token"])
        expiredAt = datetime.strptime(user.get("apiToken", {}).get("expiresAt", "-"), "%Y-%m-%dT%H:%M:%SZ")
        expiredDate = format_datetime(expiredAt, "d MMMM y 'Pukul' HH:mm:ss", locale="id_ID")

        table = Table(title="Detail User")
        table.add_column("email", style="yellow", no_wrap=True)
        table.add_column("Nama Lengkap", style="yellow", no_wrap=True)
        table.add_column("scope", style="blue", no_wrap=True)
        table.add_column("Level", style="blue", no_wrap=True)
        table.add_column("Tanggal Expired Token", style="green", no_wrap=True)

        table.add_row(
            user.get("email", "-"),
            user.get("fullName", "-"),
            user.get("scope", "-"),
            user.get("lowestRole", "-"),
            expiredDate
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
            # console.print("[blue]Detail User belum tersedia.[/blue]")
            detail_user(cfg)
        elif choice == "4":
            console.print("[blue]Generate Report belum tersedia.[/blue]")
        elif choice == "5":
            console.print("[bold red]Exiting...[/bold red]")
            sys.exit(0)
        else:
            console.print("[red]Pilihan tidak valid. Silakan coba lagi.[/red]")

if __name__ == "__main__":
    main()