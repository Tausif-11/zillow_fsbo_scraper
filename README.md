# Zillow FSBO Multi-Page Lead Scraper

An industrial-grade, high-performance asynchronous web scraping pipeline engineered to extract **For Sale By Owner (FSBO)** property leads from Zillow across large geographic target grids. Built completely on top of network-layer traffic interception to bypass strict anti-bot protections without the heavy overhead or detection profiles of Selenium or Puppeteer.

## 🚀 Key Features
- **Fingerprint Spoofing & Session Persistence:** Utilizes `tls_client` to mimic legitimate browser configurations (`chrome_120`), handling complex TLS handshakes and automated JA3 fingerprinting.
- **Dynamic Multi-Page Pagination Control:** Intercepts Zillow's backend JSON API requests (`/async-create-search-page-state`) to handle deep pagination rules gracefully.
- **Smart-Break Loop Protection:** Detects if the target gateway starts feeding duplicate payload listings on higher page matrices and automatically terminates execution early to save bandwidth.
- **Split-Routing Field Extraction:** Uses regex pattern verification to cleanly isolate actual financial **Price Reductions** from Zillow's fallback **Marketing Features** (e.g., separating price cuts from descriptions like "Waterfront lot").
- **Formatted Business Deliverables:** Compiles clean raw datasets in `.csv` alongside a fully styled, color-coded zebra-striped corporate tracking spreadsheet in `.xlsx` utilizing `openpyxl`.

## 🛠️ Tech Stack & Dependencies
- **Core Engine:** Python 3.11+
- **Network Session Handling:** `tls_client`
- **Data Architecture:** `pandas`
- **Excel Matrix Structuring:** `openpyxl`
- **Sub-dependencies:** `typing-extensions`

## 📦 Project Directory Layout
```text
zillow_fsbo_scraper/
│
├── exports/                 # Local data target storage outputs (Git ignored)
│   ├── zillow_fsbo_leads.csv
│   └── zillow_fsbo_leads.xlsx
│
├── config.py                # Secret active browser headers & cookie maps (Git ignored)
├── config.example.py        # Blank template for production workspace replication
├── main.py                  # Core execution loops, timing profiles & pipeline flow control
├── scraper.py               # Network transport configuration and target API requests
├── pipeline.py              # Parsing rules, data transformation, and openpyxl styling
├── requirements.txt         # Automated package install definitions
├── .gitignore               # System pattern security tracking definitions
└── LICENSE                  # Legal MIT distribution permissions framework