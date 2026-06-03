# Public template for tracking environment parameters
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "Origin": "https://www.zillow.com",
    "Referer": "https://www.zillow.com/homes/fsbo/",
}

COOKIES = {
    "zguid": "YOUR_ZGUID_HERE",
    # Paste remaining authentication cookies inside config.py
}

MAP_BOUNDS = {
    "north": 30.536927206387563,
    "south": 29.20321516958288,
    "east": -93.91581424044553,
    "west": -96.82993777560178
}