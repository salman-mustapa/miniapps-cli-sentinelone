import api
from datetime import datetime
from rich.console import Console
from babel.dates import format_datetime
from rich.table import Table

console = Console()

def detail_user(cfg):
    """
    Fungsi untuk menampilkan detail user
    Args:
        cfg (dict): dictionary berisi base_url dan api_token
    """
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