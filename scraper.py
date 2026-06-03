import json
import tls_client
import config

def fetch_fsbo_page(page_number=1):
    """
    Dynamically routes a mock browser connection to Zillow's 
    internal search endpoint for a specific targeted result page.
    """
    session = tls_client.Session(
        client_identifier="chrome_120",
        random_tls_extension_order=True
    )
    
    url = "https://www.zillow.com/async-create-search-page-state"
    
    # Structural correction payload built to prevent backend HTTP 400 routing rejections
    payload = {
        "searchQueryState": {
            "isMapVisible": False,
            "isListVisible": True,
            "mapBounds": config.MAP_BOUNDS,
            "filterState": {
                "sortSelection": {"value": "pricea"},
                "isForSaleByAgent": {"value": False},
                "isForSaleByOwner": {"value": True},
                "isNewConstruction": {"value": False},
                "isAuction": {"value": False},
                "isComingSoon": {"value": False},
                "isForSaleForeclosure": {"value": False}
            },
            "category": "cat2",
            "pagination": {"currentPage": page_number}  # Standardized production property tracking hook
        },
        "wants": {
            "cat2": ["listResults"],
            "cat1": ["total"]
        },
        "requestId": 25 + page_number,
        # Mandatory routing context parameter to satisfy API structural validation checks
        "searchPageSeoObject": {
            "baseUrl": "/homes/fsbo/"
        }
    }
    
    session.cookies.update(config.COOKIES)
    
    print(f"[*] Dispatching fingerprint-spoofed PUT request for [PAGE {page_number}]...")
    response = session.put(url, headers=config.HEADERS, json=payload)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 400:
        # Diagnostic traceback catch to print out exact payload errors if returned by server
        print(f"[-] Server Response Payload Check: {response.text}")
        raise ValueError("[-] API Gateway threw 400 Bad Request. Internal payload tracking syntax schema mismatch.")
    elif response.status_code == 403:
        raise PermissionError(f"[-] Blocked on Page {page_number}: Session cookies have expired. Refresh config.py.")
    else:
        raise ConnectionError(f"[-] Gateway returned anomalous status signature on page {page_number}: {response.status_code}")