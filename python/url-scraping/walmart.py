from bs4 import BeautifulSoup
import re
import json
import logging

def scrape(session, url):
    """
    Scrapes a single Walmart product page using a provided requests.Session.
    This version includes robust description extraction.
    
    Args:
        session (requests.Session): The session object with headers.
        url (str): The Walmart product URL.

    Returns:
        dict: A dictionary containing the scraped product data.
    """
    try:
        response = session.get(url, timeout=20)
        response.raise_for_status()
    except Exception as e:
        logging.error(f"Error fetching Walmart URL {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'lxml')
    
    # The most reliable data is in the __NEXT_DATA__ JSON blob
    json_data = {}
    script_tag = soup.find('script', id='__NEXT_DATA__')
    if script_tag:
        try:
            json_data = json.loads(script_tag.string)
        except json.JSONDecodeError:
            logging.warning("Failed to parse Walmart's JSON data blob.")

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
            return preprocess_string(soup.select_one(selector).get_text(strip=True))
        except AttributeError:
            return "N/A"

    def _get_price():
        return _get_text('span[itemprop="price"]')

    def _get_images():
        urls = set()
        try:
            # Navigate through the complex JSON structure to find the image list
            images = json_data['props']['pageProps']['initialData']['data']['product']['imageInfo']['allImages']
            for img in images:
                urls.add(img['url']) # Get the largest available image URL
        except (KeyError, TypeError) as e:
            logging.warning(f"Could not find images in JSON data: {e}")
        return sorted(list(urls))

    def _get_description():
        """
        Robustly extracts the description from the JSON data, falling back to HTML.
        """
        try:
            # The description is often in the 'longDescription' or 'shortDescription' field
            desc_html = (
                json_data.get('props', {}).get('pageProps', {}).get('initialData', {})
                .get('data', {}).get('product', {}).get('longDescription') or
                json_data.get('props', {}).get('pageProps', {}).get('initialData', {})
                .get('data', {}).get('product', {}).get('shortDescription')
            )
            if desc_html:
                # Clean the HTML tags from the description
                desc_soup = BeautifulSoup(desc_html, 'lxml')
                text = desc_soup.get_text(separator='\n').strip()
                return preprocess_string(text)
        except (KeyError, TypeError) as e:
            logging.warning(f"Could not find description in JSON data: {e}")
        
        # Fallback to searching common HTML selectors if JSON fails
        # text = 
        return _get_text('div.about-item-description') or _get_text('div[itemprop="description"]')

    # --- Scrape Data ---
    
    product_id_match = re.search(r'/(\d+)$', url.split('?')[0])

    product_data = {
        'site': 'Walmart',
        'title': _get_text('h1[itemprop="name"]'),
        'about': '',
        'price': _get_price(),
        'rating': _get_text('span.average-rating'),
        'number_of_reviews': _get_text('span.hidden-mobile.sub-title').split(' ')[0],
        'image_urls': _get_images(),
        'description': _get_description(),
        'product_id': product_id_match.group(1) if product_id_match else "N/A"
    }
    return product_data