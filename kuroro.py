import requests
from colorama import Fore, Style
import time
import os
from datetime import datetime
import sys  # import sys module

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://ranch.kuroro.com',
    'Pragma': 'no-cache',
    'Referer': 'https://ranch.kuroro.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 13; M2012K11AG Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/125.0.6422.165 Mobile'
}

def print_welcome_message():
    print(r"""      

▒█▀▀▀█ █▀▀█ ░█▀█░ ▒█▄░▒█ 
░▀▀▀▄▄ ░░▀▄ █▄▄█▄ ▒█▒█▒█ 
▒█▄▄▄█ █▄▄█ ░░░█░ ▒█░░▀█
          """)
    print(Fore.GREEN + Style.BRIGHT + "Kuroro BOT")
    print(Fore.RED + Style.BRIGHT + "Jangan di edit la bang :)\n\n")

def update_upgrade(bearer_token, upgrade_id):
    url = 'https://ranch-api.kuroro.com/api/Upgrades/BuyUpgrade'
    headers['Authorization'] = bearer_token
    payload = {
        "upgradeId": upgrade_id
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print(Fore.GREEN + f"Upgrade {upgrade_id} berhasil.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Upgrade {upgrade_id} gagal.")
        return None

def perform_action(url, action_name, payload, bearer_token):
    try:
        headers['Authorization'] = bearer_token
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print(Fore.GREEN + f"{action_name} successful!")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Failed to {action_name}: {e}")

def query_upgrades(file_path):
    upgrades = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                upgrade_id = line.strip()
                if upgrade_id:
                    upgrades.append(upgrade_id)
    except FileNotFoundError:
        print(Fore.RED + f"File {file_path} tidak ditemukan.")
    return upgrades

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def checkin(bearer_token):
    url = "https://ranch-api.kuroro.com/api/DailyStreak/ClaimDailyBonus"
    headers['Authorization'] = bearer_token  # Menetapkan nilai Authorization dari bearer_token
    
    # Mendapatkan tanggal saat ini dalam format yang diinginkan
    current_date = datetime.now().strftime("%Y-%m-%d")

    payload = {
        "date": current_date
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        print(Fore.GREEN + f"Daily bonus claimed successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Failed to claim daily bonus: {e}")

def read_bearer_tokens(file_path):
    tokens = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                token = line.strip()
                if token:
                    tokens.append(token)
    except FileNotFoundError:
        print(Fore.RED + f"File {file_path} tidak ditemukan.")
    return tokens

def animate_loading():
    chars = ["|", "/", "-", "\\"]
    for _ in range(20):
        sys.stdout.write("\r" + chars[_ % len(chars)] + " Tungguan sakedeng...")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 15 + "\r")  # Menghapus loading setelah selesai

def main():
    print_welcome_message()
    
    tokens = read_bearer_tokens('bearer.txt')
    
    if not tokens:
        print(Fore.RED + "Tidak ada token bearer yang ditemukan.")
        return
    
    upgrades_file = 'upgrades.txt'
    upgrades = query_upgrades(upgrades_file)
    
    if not upgrades:
        print(Fore.RED + f"Tidak ada upgrade yang ditemukan di {upgrades_file}.")
        return
    
    for i, bearer_token in enumerate(tokens, start=1):
        print(f"### Proses untuk Akun {i} ###")
        
        # Konfirmasi sebelum melakukan upgrade otomatis
        confirmation = input(Fore.BLACK + f"Apakah Anda ingin melakukan upgrade otomatis ? (y/n) : ").strip().lower()
        
        if confirmation == 'y':
            for upgrade_id in upgrades:
                result = update_upgrade(bearer_token, upgrade_id)
                if not result:
                    continue
                time.sleep(2)  # Delay 2 detik setiap kali melakukan upgrade
                clear_screen()  # Membersihkan layar setelah upgrade
                print_welcome_message()
        
        # Setelah selesai upgrade, tawarkan untuk melakukan Mining dan Feeding
        choice = input(Fore.BLACK + f"Apakah Anda ingin melakukan Mining dan Feeding secara otomatis ? (y/n) : ").strip().lower()
        if choice == 'y':
            perform_action("https://ranch-api.kuroro.com/api/Clicks/MiningAndFeeding", "Mining ", {"mineAmount": 100, "feedAmount": 0}, bearer_token)
            perform_action("https://ranch-api.kuroro.com/api/Clicks/MiningAndFeeding", "Feeding ", {"mineAmount": 0, "feedAmount": 10}, bearer_token)
            print(Fore.YELLOW + "Mining dan Feeding selesai.")
        elif choice == 'n':
            print(Fore.YELLOW + "Pilihan untuk Mining dan Feeding secara otomatis tidak dilakukan.")
        
        # Klaim bonus harian setelah semua operasi selesai
        checkin(bearer_token)
        
        # Menampilkan pesan akun selesai dan animasi
        print(Fore.BLUE + f"Akun {i} selesai, Lanjut ke akun selanjutnya")
        animate_loading()
        
        # Delay sebelum melanjutkan ke akun berikutnya
        time.sleep(5)  # Delay 5 detik sebelum lanjut ke akun selanjutnya
    
    print(Fore.BLUE + "Seluruh proses selesai.")

if __name__ == "__main__":
    main()
