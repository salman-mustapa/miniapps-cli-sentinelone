"""
SentinelOne MiniApps CLI
Copyright (c) 2025 Salman Mustapa
Released under the MIT License
https://opensource.org/licenses/MIT
"""

import json
import os

CONFIG_FILE = 'config.json'

# Fungsi untuk simpan config ke file
def save_config(base_url, api_token):
    config = {
        'base_url': base_url,
        'api_token': api_token
    }
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

# Fungsi untuk baca config dari file
def load_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)