"""
SentinelOne MiniApps CLI
Copyright (c) 2025 Salman Mustapa
Released under the MIT License
https://opensource.org/licenses/MIT
"""

import sys
import os
import pyfiglet
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from datetime import datetime
from babel.dates import format_datetime

import api
import config

console = Console()


# ─────────────────────────────────────────────
# HEADER & FOOTER
# ─────────────────────────────────────────────
def show_header():
    """Tampilkan judul aplikasi"""
    ascii_banner = pyfiglet.figlet_format("SentinelOne CLI", font="slant")
    console.print(Panel(ascii_banner, style="bold cyan", subtitle="Tools v1.0", subtitle_align="right"))


def show_footer():
    """Tampilkan copyright & lisensi"""
    console.print("\n[dim]───────────────────────────────────────────────[/dim]")
    console.print("[green]© 2025 Salman Mustapa[/green] | [cyan]MIT License[/cyan]")
    console.print("[dim]───────────────────────────────────────────────[/dim]\n")


# ─────────────────────────────────────────────
# PAUSE & CLEAR
# ─────────────────────────────────────────────
def pause_and_clear():
    """Pause tampilan sampai user tekan Enter, lalu clear terminal"""
    input("\nPress any key to return to menu...")
    os.system("cls" if os.name == "nt" else "clear")
    show_header()


# ─────────────────────────────────────────────
# MENU UTAMA
# ─────────────────────────────────────────────
def show_menu():
    """Tampilkan menu utama"""
    menu_panel = Panel(
        "[bold white]1.[/] List Agents\n"
        "[bold white]2.[/] Detail Agent\n"
        "[bold white]3.[/] Detail User\n"
        "[bold white]4.[/] Generate Report\n"
        "[bold white]5.[/] Exit",
        title="[bold green]Menu Utama[/bold green]",
        border_style="cyan"
    )
    console.print(menu_panel)


# ─────────────────────────────────────────────
# LIST AGENTS
# ─────────────────────────────────────────────
def list_agents(cfg):
    """Tampilkan daftar agent dari API"""
    try:
        agents = api.get_agents(cfg["base_url"], cfg["api_token"])
        table = Table(title="List Agents")
        table.add_column("Endpoint Name", style="yellow")
        table.add_column("OS", style="magenta")
        table.add_column("Status", style="green")
        table.add_column("IP Address", style="cyan")

        for agent in agents:
            ip_list = []
            for iface in agent.get("networkInterfaces", []):
                ip_list.extend(iface.get("inet", []))
            ip_addr = ", ".join(ip_list) if ip_list else "-"

            table.add_row(
                agent.get("computerName", "-"),
                agent.get("osName", "-"),
                "Active" if agent.get("isActive", False) else "Inactive",
                ip_addr
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error Load Data: {e}[/red]")


# ─────────────────────────────────────────────
# DETAIL USER
# ─────────────────────────────────────────────
def detail_user(cfg):
    """Tampilkan detail user dari API"""
    try:
        user = api.get_user_details(cfg["base_url"], cfg["api_token"])
        expired_at_str = user.get("apiToken", {}).get("expiresAt", "-")
        expired_at = datetime.strptime(expired_at_str, "%Y-%m-%dT%H:%M:%SZ") if expired_at_str != "-" else "-"
        expired_date = format_datetime(expired_at, "d MMMM y', Pukul' HH:mm:ss", locale="id_ID") if expired_at != "-" else "-"

        table = Table(title="Detail User")
        table.add_column("Variabel", style="white")
        table.add_column("Data", style="green")

        table.add_row("Email", user.get("email", "-"))
        table.add_row("Nama Lengkap", user.get("fullName", "-"))
        table.add_row("Scope", user.get("scope", "-"))
        table.add_row("Role", user.get("lowestRole", "-"))
        table.add_row("Token Expired", expired_date)

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error Load Data: {e}[/red]")


# ─────────────────────────────────────────────
# MAIN FUNCTION
# ─────────────────────────────────────────────
def main():
    """Entry point program CLI"""
    show_header()

    # Load config, jika tidak ada minta input user
    cfg = config.load_config()
    if not cfg:
        console.print("[yellow]File config tidak ditemukan.[/yellow]")
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
            pause_and_clear()
        elif choice == "2":
            console.print("[blue]Detail Agent belum tersedia.[/blue]")
            pause_and_clear()
        elif choice == "3":
            detail_user(cfg)
            pause_and_clear()
        elif choice == "4":
            console.print("[blue]Generate Report belum tersedia.[/blue]")
            pause_and_clear()
        elif choice == "5":
            console.print("[bold red]Exiting...[/bold red]")
            show_footer()
            sys.exit(0)
        else:
            console.print("[red]Pilihan tidak valid. Silakan coba lagi.[/red]")


if __name__ == "__main__":
    main()
