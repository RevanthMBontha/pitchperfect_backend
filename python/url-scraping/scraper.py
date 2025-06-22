import argparse
import logging
import json
import time
import random
from urllib.parse import urlparse
import requests
import sys

# Import the scraping modules
import amazon
import walmart

url = sys.argv[1]

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Map hostnames to their respective scraper modules
SCRAPER_MAPPING = {
    'www.amazon.in': amazon,
    'www.amazon.com': amazon,
    'www.walmart.com': walmart,
}

def get_scraper_for_url(url):
    """Determines which scraper to use based on the domain name."""
    hostname = urlparse(url).hostname
    return SCRAPER_MAPPING.get(hostname)

def main(url, output=None):
    """Main function to initialize and run the scraper with retries."""
    
    scraper_module = get_scraper_for_url(url)

    if not scraper_module:
        logging.error(f"No scraper available for the URL hostname: {urlparse(url).hostname}")
        return

    # Create a requests.Session to persist headers and cookies
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Connection": "keep-alive",
    })

    logging.info(f"Using {scraper_module.__name__} scraper for: {url}")
    
    product_details = None
    retries = 3
    for attempt in range(retries):
        try:
            # Pass the session to the scraper module
            product_details = scraper_module.scrape(session, url)
            if product_details:
                break # Success, exit the loop
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {attempt + 1} of {retries} failed: {e}")
            if attempt < retries - 1:
                time.sleep(3) # Wait for 3 seconds before retrying
            else:
                logging.error("All retry attempts failed.")

    if product_details:
        logging.info("Successfully scraped product data.")
        try:
            # with open(output, 'w', encoding='utf-8') as f:
            #     json.dump(product_details, f, indent=4, ensure_ascii=False)
            # logging.info(f"Data saved to {output}")
            
            print(json.dumps(product_details, indent=4, ensure_ascii=False))
            return product_details

        except IOError as e:
            logging.error(f"Failed to write data to file: {e}")
    else:
        logging.error("Failed to retrieve product details after all attempts.")
        return {}

if __name__ == "__main__":
    # url = "https://www.amazon.in/Philips-Trimmer-BeardSense-Technology-Patentented/dp/B0CHS1BP2B/?_encoding=UTF8&pd_rd_w=XFrz4&content-id=amzn1.sym.509965a2-791b-4055-b876-943397d37ed3%3Aamzn1.symc.fc11ad14-99c1-406b-aa77-051d0ba1aade&pf_rd_p=509965a2-791b-4055-b876-943397d37ed3&pf_rd_r=E92ZRGPB6CBSX3KR11GH&pd_rd_wg=nw7od&pd_rd_r=5269a901-ba7f-42df-92ac-de6fce035ce7&ref_=pd_hp_d_atf_ci_mcx_mr_ca_hp_atf_d"
    # url = "https://www.amazon.in/Shaping-Transparent-Anti-Redness-Sensitive-Calming/dp/B0BKL6C219/ref=srd_d_psims_d_sccl_2_2/262-1167329-7517349?pd_rd_w=SSjno&content-id=amzn1.sym.6b3aa144-fd3f-4cac-9ae1-ac2407bcccc2&pf_rd_p=6b3aa144-fd3f-4cac-9ae1-ac2407bcccc2&pf_rd_r=H4KNY0T523DS9FNZRARA&pd_rd_wg=OQON7&pd_rd_r=c0a8f6ee-0cfe-4a12-aec8-6120f022bb9c&pd_rd_i=B0BKL6C219&th=1"
    url = sys.argv[1]
    main(url)