# Magnet2RD

Magnet2RD is a powerful, lightweight tool that converts Torrent Magnet Links into high-speed, direct download links using the [Real Debrid](https://real-debrid.com/) API. 

It is available as both a **Command Line Interface (CLI)** and a **Modern Static Web App**.

---

## ✨ Features

- **Instant Conversion**: Paste a magnet link, get a direct download link instantly.
- **Auto-Selection**: Automatically identifies and selects the largest video file (the main movie) in a torrent.
- **High Speed**: Leverages Real Debrid's high-speed servers for your downloads.
- **Glassmorphic UI**: (Web) A premium, modern interface with smooth animations.
- **Secure**: 
  - (CLI) Uses environment variables (`.env`) for API safety.
  - (Web) Stores your token only in your browser's `localStorage`.

---

## 🌐 Web App (Recommended)

The web app provides a user-friendly interface that can be hosted on GitHub Pages.

### How to Run Locally
1. Ensure you have Node.js installed.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Open the provided `localhost` URL in your browser.

### Deployment
1. Build the production files:
   ```bash
   npm run build
   ```
2. The `dist/` folder contains the ready-to-host static files.

---

## 🖥️ Command Line Interface (CLI)

For those who prefer the terminal.

### Prerequisites
- Python 3.x installed.
- `requests` and `python-dotenv` packages.

### Installation & Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the root directory:
   ```env
   RD_API_TOKEN=your_real_debrid_api_token_here
   ```
3. Run the tool:
   ```bash
   python main.py
   ```
4. Enter your magnet link and download directory.
5. Wait for the download to complete.

---

## ⚠️ Disclaimer

This tool is for educational purposes only. Use it responsibly and in accordance with Real Debrid's Terms of Service.

&copy; 2025 [NassosKranidiotis](https://nassoskranidiotis.com). All rights reserved.