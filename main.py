import requests
import time
import os
from dotenv import load_dotenv

# Load the secrets from the .env file
load_dotenv()

# --- CONFIGURATION ---
RD_API_TOKEN = os.getenv("RD_API_TOKEN").strip()

def get_direct_link(magnet_link):
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
    
    # We might need a small delay for RD to parse the metadata
    attempts = 0
    while attempts < 10:
        info = requests.get(info_url, headers=headers).json()
        if info['status'] == 'waiting_files_selection':
            break
        time.sleep(1)
        attempts += 1

    # Find largest file ID
    files = info['files']
    # Sort files by size (largest first)
    sorted_files = sorted(files, key=lambda x: x['bytes'], reverse=True)
    largest_file_id = sorted_files[0]['id']
    
    # 3. Select the file
    select_url = f"https://api.real-debrid.com/rest/1.0/torrents/selectFiles/{torrent_id}"
    requests.post(select_url, headers=headers, data={"files": largest_file_id})
    
    # 4. Get the Download Link
    print(f"--> 3. Getting download link...")
    # Refresh info to get the 'links' array
    info = requests.get(info_url, headers=headers).json()
    
    if len(info['links']) > 0:
        rd_link = info['links'][0] # The protected link
        
        # 5. Unrestrict the link (The final step)
        print(f"--> 4. Unrestricting link (Making it downloadable)...")
        unrestrict_url = "https://api.real-debrid.com/rest/1.0/unrestrict/link"
        unrestrict_resp = requests.post(unrestrict_url, headers=headers, data={"link": rd_link})
        
        if unrestrict_resp.status_code == 200:
            final_link = unrestrict_resp.json()['download']
            print(f"\n[SUCCESS] Here is your DIRECT download link:\n")
            print(final_link)
            print("\n(You can paste this into a browser or a download manager)")
        else:
            print("Error unrestricting link.")
    else:
        print("Error: No links found. The torrent might not be cached instantly.")

if __name__ == "__main__":
    magnet = input("Paste Magnet Link: ").strip()
    get_direct_link(magnet)