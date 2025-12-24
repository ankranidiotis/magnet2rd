const RD_API_BASE = "https://api.real-debrid.com/rest/1.0";

// Elements
const rdTokenInput = document.getElementById('rd-token');
const magnetLinkInput = document.getElementById('magnet-link');
const convertBtn = document.getElementById('convert-btn');
const resultSection = document.getElementById('result-section');
const statusContainer = document.getElementById('status-container');
const finalLinkInput = document.getElementById('final-link');
const fileNameEl = document.getElementById('file-name');
const copyBtn = document.getElementById('copy-btn');
const downloadBtn = document.getElementById('download-btn');
const resetBtn = document.getElementById('reset-btn');

// Load token from localStorage
const savedToken = localStorage.getItem('rd_token');
if (savedToken) {
    rdTokenInput.value = savedToken;
}

// Helper: Show status message
function showStatus(message, type = 'info') {
    const div = document.createElement('div');
    div.className = `status ${type}`;
    div.textContent = message;
    statusContainer.innerHTML = '';
    statusContainer.appendChild(div);
}

// Helper: API Request
async function rdRequest(endpoint, method = 'GET', body = null) {
    const token = rdTokenInput.value.trim();
    if (!token) throw new Error("API Token is required");

    // Save token
    localStorage.setItem('rd_token', token);

    const headers = {
        "Authorization": `Bearer ${token}`
    };

    const options = {
        method,
        headers
    };

    if (body) {
        options.body = new URLSearchParams(body);
    }

    try {
        const response = await fetch(`${RD_API_BASE}${endpoint}`, options);
        if (!response.ok) {
            const errData = await response.json().catch(() => ({}));
            throw new Error(errData.error || `HTTP Error ${response.status}`);
        }
        if (response.status === 204) return null;
        return await response.json();
    } catch (err) {
        if (err.message.includes('Failed to fetch')) {
            throw new Error("CORS Error: Real-Debrid API blocked the request. Please use a CORS-unblocking browser extension or a proxy.");
        }
        throw err;
    }
}

async function convertMagnet() {
    const magnet = magnetLinkInput.value.trim();
    if (!magnet) return showStatus("Please paste a magnet link", "error");

    // UI State
    convertBtn.disabled = true;
    convertBtn.querySelector('.btn-text').textContent = "Processing...";
    convertBtn.querySelector('.loader').classList.remove('hidden');
    statusContainer.innerHTML = '';

    try {
        // 1. Add Magnet
        showStatus("Step 1: Adding magnet to Real-Debrid...");
        const addResp = await rdRequest("/torrents/addMagnet", "POST", { magnet });
        const torrentId = addResp.id;

        // 2. Get Info and wait for file selection
        showStatus("Step 2: Parsing metadata...");
        let info;
        let attempts = 0;
        while (attempts < 15) {
            info = await rdRequest(`/torrents/info/${torrentId}`);
            if (info.status === 'waiting_files_selection') break;
            if (info.status === 'error') throw new Error("Real-Debrid error while parsing magnet.");
            await new Promise(r => setTimeout(r, 1000));
            attempts++;
        }

        if (info.status !== 'waiting_files_selection') {
            throw new Error("Timeout waiting for metadata selection.");
        }

        // 3. Select largest file
        showStatus("Step 3: Selecting main file...");
        const files = info.files.sort((a, b) => b.bytes - a.bytes);
        const largestFileId = files[0].id;
        await rdRequest(`/torrents/selectFiles/${torrentId}`, "POST", { files: largestFileId });

        // 4. Get the link
        showStatus("Step 4: Generating download links...");
        // Wait a bit for processing
        await new Promise(r => setTimeout(r, 2000));
        info = await rdRequest(`/torrents/info/${torrentId}`);

        if (!info.links || info.links.length === 0) {
            throw new Error("No links found for this torrent.");
        }
        const rdLink = info.links[0];

        // 5. Unrestrict link
        showStatus("Step 5: Unrestricting link...");
        const unrestrictResp = await rdRequest("/unrestrict/link", "POST", { link: rdLink });

        // Success!
        fileNameEl.textContent = unrestrictResp.filename || "Your file is ready";
        finalLinkInput.value = unrestrictResp.download;
        downloadBtn.href = unrestrictResp.download;

        resultSection.classList.remove('hidden');
        convertBtn.classList.add('hidden');
        showStatus("Success!", "info");

    } catch (err) {
        showStatus(err.message, "error");
        console.error(err);
    } finally {
        convertBtn.disabled = false;
        convertBtn.querySelector('.btn-text').textContent = "Generate Direct Link";
        convertBtn.querySelector('.loader').classList.add('hidden');
    }
}

// Events
convertBtn.addEventListener('click', convertMagnet);

copyBtn.addEventListener('click', () => {
    finalLinkInput.select();
    document.execCommand('copy');
    const originalText = copyBtn.textContent;
    copyBtn.textContent = "Copied!";
    setTimeout(() => copyBtn.textContent = originalText, 2000);
});

resetBtn.addEventListener('click', () => {
    resultSection.classList.add('hidden');
    convertBtn.classList.remove('hidden');
    magnetLinkInput.value = '';
    statusContainer.innerHTML = '';
});
