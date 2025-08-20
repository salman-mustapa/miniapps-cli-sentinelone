from rich.console import Console
from rich.table import Table
import api

console = Console()

def list_agents(cfg):
    """
    Fungsi untuk menampilkan list agent dari SentinelOne API dengan pagination
    menggunakan cursor

    Args:
        cfg (dict): dictionary berisi base_url dan api_token
    """
    try:
        # Inisialisasi Variabel
        base_url = cfg["base_url"]
        api_token = cfg["api_token"]
        cursor = ""
        limit = 2
        shown = 0
        total_items = 0
        page = 1

        while True:
            # Ambil data agents sesuai limit
            response = api.get_agents(base_url, api_token, limit=limit, cursor=cursor)
            agents = response.get("data", [])
            pagination = response.get("pagination", {})
            total_items += pagination.get("totalItems", 0)
            next_cursor = pagination.get("nextCursor", None)

            # Buat tabll untuk menampilkan data agents
            table = Table(title=f"List Agents", show_lines=True)
            table.add_column("No", style="cyan")
            table.add_column("Endpoint Name", style="yellow")
            table.add_column("OS", style="magenta")
            table.add_column("Status", style="green")
            table.add_column("IP Address", style="cyan")

            for no_urut, agent in enumerate(agents, start=1):
                ipv4_list = []                
                for iface in agent.get("networkInterfaces", []):
                    ipv4_list.extend(iface.get("inet", []))

                # Inisialisasi Variable
                computerName = agent.get("computerName", "-")
                osName = agent.get("osName", "-")
                isActive = "Active" if agent.get("isActive", False) else "Inactive"
                ip_address = ", ".join(ipv4_list) if ipv4_list else "-"

                table.add_row(
                    str(no_urut),
                    computerName,
                    osName,
                    isActive,
                    ip_address
                )

            # Update jumlah yang sudah ditampilkan
            shown += len(agents)
            
            if not next_cursor and shown >= total_items:
                console.print("\n[bold yellow]Tidak ada data lagi untuk ditampilkan.[/bold yellow]")
                break
            
            # Print Table
            console.print(table)
            console.print(f"[bold green]List {shown} Agent dari Total {total_items} Agent [/bold green]\n")
            
            # kalau ada maka tanya user apakah mau lanjut tampilkan data berikutnya
            lanjut = console.input("Lihat data lainnya ? (y/n): ").strip().lower()
            if lanjut == 'n':
                break
            
            # Update cursor untuk pagination
            cursor = next_cursor
            page +=1

        # # Get Response dari Api Agent
        # agents_response = api.get_agents(cfg["base_url"], cfg["api_token"])
        
        # # Ambil data agents dan totalItems
        # agents = agents_response.get("data", [])
        # totalItems = agents_response.get("pagination", {}).get("totalItems", len(agents))


        # table = Table(title=f"List Agents", show_lines=True)
        # table.add_column("No", style="cyan")
        # table.add_column("Endpoint Name", style="yellow")
        # table.add_column("OS", style="magenta")
        # table.add_column("Status", style="green")
        # table.add_column("IP Address", style="cyan")

        # for no_urut, agent in enumerate(agents, start=1):
        #     ipv4_list = []
        #     for iface in agent.get("networkInterfaces", []):
        #         ipv4_list.extend(iface.get("inet", []))
        #     ip_address = ", ".join(ipv4_list) if ipv4_list else "-"

        #     table.add_row(
        #         str(no_urut),
        #         agent.get("computerName", "-"),
        #         agent.get("osName", "-"),
        #         "Active" if agent.get("isActive", False) else "Inactive",
        #         ip_address
        #     )

        # console.print(table)
        # console.print(f"[bold green]List {len(agents)} Agent dari Total {totalItems} Agent")

    except Exception as e:
        console.print(f"[red]Error Load Data: {e}[/red]")