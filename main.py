import sys
import pyfiglet
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

# Import menu dari folder CLI
from cli import list_agents, detail_user, generate_report

# import api
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
            # console.print("[blue]Generate Report belum tersedia.[/blue]")
            generate_report(cfg)
            pause_and_clear()
        elif choice == "5":
            console.print("[bold red]Exiting...[/bold red]")
            show_footer()
            sys.exit(0)
        else:
            console.print("[red]Pilihan tidak valid. Silakan coba lagi.[/red]")


if __name__ == "__main__":
    main()

    