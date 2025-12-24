import requests
import time
import os
from dotenv import load_dotenv
from tqdm import tqdm

# Load the secrets from the .env file
load_dotenv()

# --- CONFIGURATION ---
RD_API_TOKEN = os.getenv("RD_API_TOKEN").strip()

def download_video(url, destination_folder, filename):
    """Κατεβάζει το αρχείο με progress bar στο ορισμένο path."""
    # Δημιουργία φακέλου αν δεν υπάρχει
    os.makedirs(destination_folder, exist_ok=True)
    
    full_path = os.path.join(destination_folder, filename)
    
    print(f"\n--> 5. Downloading file to: {full_path}")
    
    # Ξεκινάμε τη λήψη με stream=True για μεγάλα αρχεία
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(full_path, 'wb') as file, tqdm(
        desc=filename[:30] + '...', # Μικραίνουμε το όνομα για να χωράει στο CLI
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024 * 1024): # 1MB chunks
            size = file.write(data)
            bar.update(size)
    
    print(f"\n[DONE] Download complete!")

def get_direct_link(magnet_link, download_dir):
    headers = {"Authorization": f"Bearer {RD_API_TOKEN}"}
    
    # 1. Add Magnet
    print(f"--> 1. Adding Magnet...")
    add_url = "https://api.real-debrid.com/rest/1.0/torrents/addMagnet"
    resp = requests.post(add_url, headers=headers, data={"magnet": magnet_link})
    
    if resp.status_code != 201:
        print(f"Error adding magnet: {resp.status_code}")
        return
        
    torrent_id = resp.json()['id']
    print(f"    (ID: {torrent_id})")

    # 2. Get File Info to find the largest file (The Movie)
    print(f"--> 2. Selecting main file...")
    info_url = f"https://api.real-debrid.com/rest/1.0/torrents/info/{torrent_id}"
    
    attempts = 0
    while attempts < 15:
        info_resp = requests.get(info_url, headers=headers)
        info = info_resp.json()
        if info['status'] == 'waiting_files_selection':
            break
        # Αν είναι ήδη έτοιμο (π.χ. instant cached)
        if info['status'] in ['downloaded', 'uploading']:
            break
        time.sleep(1)
        attempts += 1

    # Find largest file ID
    files = info.get('files', [])
    if not files:
        print("Error: Could not retrieve file list.")
        return

    sorted_files = sorted(files, key=lambda x: x['bytes'], reverse=True)
    largest_file_id = sorted_files[0]['id']
    
    # 3. Select the file
    select_url = f"https://api.real-debrid.com/rest/1.0/torrents/selectFiles/{torrent_id}"
    requests.post(select_url, headers=headers, data={"files": largest_file_id})
    
    # Περιμένουμε λίγο να γίνει "downloaded" στον server της RD (αν είναι cached είναι ακαριαίο)
    print(f"--> 3. Processing on Real-Debrid...")
    time.sleep(2)
    info = requests.get(info_url, headers=headers).json()
    
    if len(info['links']) > 0:
        rd_link = info['links'][0] 
        
        # 4. Unrestrict the link
        print(f"--> 4. Unrestricting link...")
        unrestrict_url = "https://api.real-debrid.com/rest/1.0/unrestrict/link"
        unrestrict_resp = requests.post(unrestrict_url, headers=headers, data={"link": rd_link})
        
        if unrestrict_resp.status_code == 200:
            data = unrestrict_resp.json()
            final_link = data['download']
            filename = data['filename'] # Παίρνουμε το επίσημο όνομα αρχείου από την RD
            
            print(f"\n[SUCCESS] Direct link generated.")
            
            # ΕΝΑΡΞΗ DOWNLOAD
            download_video(final_link, download_dir, filename)
        else:
            print("Error unrestricting link.")
    else:
        print("Error: No links found. If this is a new torrent, it might still be downloading to Real-Debrid servers.")

if __name__ == "__main__":
    magnet = input("Paste Magnet Link: ").strip()
    folder = input("Enter Download Directory (e.g. ./downloads): ").strip()
    
    if not folder:
        folder = "/home/media/movies/" # Default φάκελος αν πατήσεις Enter
        
    get_direct_link(magnet, folder)