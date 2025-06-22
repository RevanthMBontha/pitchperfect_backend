from bs4 import BeautifulSoup
import re
import json
import logging

def scrape(session, url):
    """
    Scrapes a single Amazon product page using a provided requests.Session.
    This version correctly targets the image gallery and deduplicates images.
    
    Args:
        session (requests.Session): The session object with headers.
        url (str): The Amazon product URL.

    Returns:
        dict: A dictionary containing the scraped product data.
    """
    try:
        response = session.get(url, timeout=20)
        response.raise_for_status()
    except Exception as e:
        logging.error(f"Error fetching Amazon URL {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'lxml')
    
    # --- Data Extraction Functions ---

    def preprocess_string(text):
        """
        Removes leading, trailing, and extra spaces within a string.
        """
        try:
            return " ".join(text.split())
        except Exception as e:
            print(f"Exception encountered while preprocess_strings - {e}")
            return text

    def _get_text(selector):
        try:
            return soup.select_one(selector).get_text(strip=True)
        except AttributeError:
            return "N/A"

    def _get_price():
        price = _get_text('span.a-offscreen')
        return re.sub(r'[^0-9.]', '', price).strip('.') if price != "N/A" else "N/A"

    def _get_images():
        """
        Correctly extracts all unique, high-resolution images from the gallery data.
        """
        image_urls = {}
        
        # This script block contains the data for the entire image gallery.
        script_tags = soup.find_all('script', type='text/javascript')
        for script in script_tags:
            # We look for the 'colorImages' block which holds the gallery.
            if script.string and 'colorImages' in script.string:
                # This regex finds all image variants ('main', 'large', 'hiRes') in the script.
                matches = re.findall(r'"(https://m\.media-amazon\.com/images/I/.*?)"', script.string)
                for url in matches:
                    # Filter out any low-resolution thumbnails
                    if '._' in url.rsplit('/', 1)[-1]:
                        continue
                    
                    # Extract the unique base name of the image (e.g., '61qvjm7QQiL')
                    base_name_match = re.search(r'/I/([A-Za-z0-9-_]+)', url)
                    if base_name_match:
                        base_name = base_name_match.group(1)
                        # We only want to store one URL per unique image.
                        # Since we are iterating through the variants, the last one found is often the highest res.
                        # We simply store the URL against its unique base name.
                        image_urls[base_name] = url
                # Once we've found and processed the main gallery, we can stop.
                if image_urls:
                    break
                        
        return sorted(list(image_urls.values()))

    def _get_about_the_product():
        bullets = soup.select('#feature-bullets li span.a-list-item')
        about = "\n".join([b.get_text(strip=True) for b in bullets]) or _get_text('#productDescription')
        return preprocess_string(about)

    def _get_description():
        description_element = soup.find('div', id='productDescription')
        if description_element:
            return preprocess_string(description_element.get_text(strip=True))
        else:
            return ""

    
    # --- Scrape Data ---
    
    asin_match = re.search(r'/dp/([A-Z0-9]{10})', url)
    
    product_data = {
        'site': 'Amazon',
        'title': _get_text('#productTitle'),
        'price': _get_price(),
        'rating': _get_text('span.a-icon-alt').split(' ')[0],
        'number_of_reviews': _get_text('#acrCustomerReviewText').split(' ')[0],
        'image_urls': _get_images(),
        'about': _get_about_the_product(),
        'description': _get_description(),
        'product_id': asin_match.group(1) if asin_match else "N/A"
    }
    return product_data