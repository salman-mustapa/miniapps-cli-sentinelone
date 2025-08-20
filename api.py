"""
SentinelOne MiniApps CLI
Copyright (c) 2025 Salman Mustapa
Released under the MIT License
https://opensource.org/licenses/MIT
"""

import requests

# Fungsi untuk ambil data agents
def get_agents(base_url, api_token, limit=10, cursor=""):
    """
    Ambil list agents dari SentinelOne API
    Args:
        base_url (str): URL dasar SentinelOne (contoh: https://xxx.sentinelone.net/web/api/v2.1)
        api_token (str): API Token user
        limit (int): jumlah maksimal agents yang diambil
    Returns:
        list: data agents dalam bentuk list of dict
    """

    url = f"{base_url}/agents?limit={limit}&cursor={cursor}"
    headers = {"Authorization": f"ApiToken {api_token}"}

    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        # Ambil data agents dari response
        """
        Response format:
        {
            "data": [
                {}
            ],
            "pagination": {
                "nextCursor": None,
                "totalItems": xx,
            }
        }
        """
        return res.json()
    else:
        raise Exception(f"Gagal ambil agents. Status code: {res.status_code}, Detail: {res.text}")

def get_user_details(base_url, api_token):
    """
    Ambil detail user dari SentinelOne API
    Args:
        base_url (str): URL dasar SentinelOne (contoh: https://xxx.sentinelone.net/web/api/v2.1)
        api_token (str): API Token user
    Returns:
        dict: data user dalam bentuk dict
    """

    url = f"{base_url}/user"
    headers = {"Authorization": f"ApiToken {api_token}"}

    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        return res.json().get("data", {})
    else:
        raise Exception(f"Gagal ambil detail user. Status code: {res.status_code}, Detail: {res.text}")