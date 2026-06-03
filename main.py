import os
import time
import random
import datetime
import pandas as pd
import scraper
import pipeline

def main():
    os.makedirs("exports", exist_ok=True)
    
    print("\n[===============================================================]")
    print("[*] INITIALIZING LIVE MULTI-PAGE ZILLOW FSBO CRAWLER WORKSPACE...")
    print("[===============================================================]\n")
    
    TARGET_PAGES = 19
    cumulative_records = []
    seen_zpids = set()  # In-memory index tracking cache to trap repeat records instantly
    
    for current_page in range(1, TARGET_PAGES + 1):
        try:
            raw_json_data = scraper.fetch_fsbo_page(page_number=current_page)
            df_page = pipeline.parse_and_transform(raw_json_data)
            
            if df_page.empty:
                print(f"[!] Warning: Extracted empty frame array on page {current_page}. Terminating loop safely.")
                break
            
            # Count how many new, unseen properties are on this page
            page_zpids = df_page['ZPID'].astype(str).tolist()
            new_listings_count = sum(1 for zpid in page_zpids if zpid not in seen_zpids)
            
            # Smart Loop Break: If a page contains 100% duplicate items, Zillow has entered a loop
            if current_page > 1 and new_listings_count == 0:
                print(f"\n[!] Smart-Break Triggered on Page {current_page}: Zillow server is repeating previous results.")
                print("[*] Terminating execution matrix early to save network bandwidth and protect session tracking tokens.\n")
                break
                
            # Update cache index tracking references
            seen_zpids.update(page_zpids)
            cumulative_records.append(df_page)
            print(f"[√] Captured Page {current_page}: Added {new_listings_count} new properties (Total unique so far: {len(seen_zpids)}).")
            
            if current_page < TARGET_PAGES:
                sleep_duration = random.uniform(4.0, 7.0)
                print(f"[*] Sleeping for {sleep_duration:.2f}s to maintain anti-bot hygiene...")
                time.sleep(sleep_duration)
                
        except Exception as e:
            print(f"\n[!] Pipeline iteration broke on Page {current_page}: {e}")
            print("[*] Compiling all successful data chunks gathered before error event...\n")
            break

    if cumulative_records:
        # Merge arrays and drop any residual duplicates safely
        df_master = pd.concat(cumulative_records, ignore_index=True)
        df_master.drop_duplicates(subset=["ZPID"], keep="first", inplace=True)
        
        csv_out = "exports/zillow_fsbo_leads.csv"
        excel_out = "exports/zillow_fsbo_leads.xlsx"
        
        # Save clean text stream
        df_master.to_csv(csv_out, index=False, encoding="utf-8")
        print(f"[√] Master raw data tracker compiled successfully -> {csv_out}")
        
        # Safe Excel Writing Wrapper with open workbook safety switches
        try:
            pipeline.save_styled_excel(df_master, excel_out)
            print(f"\n[======= PIPELINE COMPLETE: {len(df_master)} TOTAL ACTIVE LEADS COMPILED SUCCESSFULLY =======]\n")
        except PermissionError:
            print("\n[!] WARNING: 'zillow_fsbo_leads.xlsx' is currently open in Excel and locked.")
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            fallback_excel = f"exports/zillow_fsbo_leads_{timestamp}.xlsx"
            print(f"[*] Routing fallback recovery engine to alternate destination asset...")
            pipeline.save_styled_excel(df_master, fallback_excel)
            print(f"\n[======= PIPELINE COMPLETE (WITH FALLBACK): {len(df_master)} LEADS SAVED TO {fallback_excel} =======]\n")
    else:
        print("[-] Complete pipeline runtime asset failure: Zero data blocks recovered.")

if __name__ == "__main__":
    main()