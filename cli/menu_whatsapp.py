from rich.console import Console

console = Console()

def send_whatsapp_report(file_path, recipient_number):
    """
    Fungsi dummy untuk kirim report ke WhatsApp Gateway
    Args:
        file_path (str): path file report
        recipient_number (str): nomor tujuan
    """
    console.print(f"[blue]Report {file_path} akan dikirim ke {recipient_number} (dummy)[/blue]")
