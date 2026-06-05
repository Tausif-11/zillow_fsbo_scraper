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
├── .github/
│   └── workflows/
│       └── python-app.yml       # Production CI/CD workflow validation automation
│
├── exports/                     # Local extracted data targets folder (Git ignored)
│   ├── zillow_fsbo_leads.csv
│   └── zillow_fsbo_leads.xlsx
│
├── venv/                        # Local Python Virtual Environment folder (Git ignored)
│
├── .gitignore                   # System filter rules file ensuring credential secrecy
├── LICENSE                      # Clear MIT Legal Permissions framework file
├── README.md                    # Professional Markdown portfolio documentation file
├── test_pipeline.py             # Automated data integrity unit tests for GitHub Actions
│
├── main.py                      # Master script execution loops, logic, and timers
├── scraper.py                   # Network transport configuration engine (`tls_client`)
├── pipeline.py                  # Parsing layer, regex split-routing & openpyxl styling
│
├── config.py                    # Private cookies, active tokens, and target headers (Git ignored)
├── config.example.py            # Public placeholder blueprint for production cloning
└── requirements.txt             # Third-party module installation tracking index
