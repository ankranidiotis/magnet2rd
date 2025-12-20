# Real Debrid Magnet Unrestricter (CLI)

A lightweight Python command-line tool that automatically converts Torrent Magnet Links into high-speed, direct download links using the [Real Debrid](https://real-debrid.com/) API.

This tool automates the manual workflow:
1.  **Adds** the magnet link to your Real Debrid cloud.
2.  **Selects** the largest file (usually the main movie) automatically.
3.  **Unrestricts** the link to generate a direct HTTPs download URL.

> **Note:** This tool bypasses the common `403 Forbidden` errors on the `/instantAvailability` endpoint by using the direct "Add & Check" method.

## 🚀 Features

* **Instant Conversion:** Paste a magnet link, get a direct download link.
* **Auto-Selection:** automatically identifies and selects the largest video file in a torrent.
* **Secure:** Uses environment variables to keep your API Token safe.
* **Lightweight:** Runs entirely in the terminal with minimal dependencies.

## 🛠️ Prerequisites

* Python 3.x installed.
* A Premium [Real Debrid](https://real-debrid.com/) account.
* Your API Token (Get it from [https://real-debrid.com/apitoken](https://real-debrid.com/apitoken)).

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/rd-magnet-unrestricter.git](https://github.com/YOUR_USERNAME/rd-magnet-unrestricter.git)
    cd rd-magnet-unrestricter
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Security:**
    * Create a file named `.env` in the root folder.
    * Add your API token inside it:
        ```ini
        RD_API_TOKEN=your_real_debrid_api_token_here
        ```
    * *Note: This file is ignored by Git to protect your account.*

## 🖥️ Usage

Run the script from your terminal:

```bash
python main.py