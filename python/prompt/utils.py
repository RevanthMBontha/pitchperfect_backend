import json
import requests
import numpy as np
import re
import os

def load_json_file(filepath):
    data = None
    try:
        if filepath.endswith("json"):
            with open(filepath, 'r') as file:
                data = json.load(file)
    except Exception as e:
        pass
        print(f"Exception encountered while loading the json file - {e}")
    return data

# def get_unique_image_urls(image_urls):
    """
    Returns a sorted list of unique image URLs.
    
    Args:
        image_urls (set): A set of image URLs.
        
    Returns:
        list: A sorted list of unique image URLs.
    """
    unique_hashes = {}
    unique_images = []
    for url in tqdm(image_urls):
        response = requests.get(url)
        if response.status_code == 200: 
            arr = np.asarray(bytearray(response.content), dtype=np.uint8)
            image = cv2.imdecode(arr, -1)
            image_shape = image.shape
            if image_shape[0] < 100 or image_shape[1] < 100:
                continue
            
            image = Image.open(BytesIO(response.content)).convert("RGB")    
            hash_val = imagehash.phash(image)
            if hash_val not in unique_hashes:
                unique_hashes[hash_val] = url
                unique_images.append(url)
    return unique_images

def preprocess_string(text):
    """
    Removes leading, trailing, and extra spaces within a string.
    """
    try:
        return " ".join(text.split())
    except Exception as e:
        print(f"Exception encountered while preprocess_strings - {e}")
        return text
    
def clean_text(text):
    return text.replace("\n", " ").replace("\t", " ").replace("\\", "").strip()

def write_recommendations_to_json(output, output_filename):
    with open(output_filename, 'w') as file:
        json.dump(output, file, indent=4)
    return

def get_api_token():
    """
    Retrieves the API token from an environment variable.
    
    Returns:
        str: The API token.
    """
    import os
    return os.getenv("API_TOKEN", DEFAULT_OPEN_API_KEY)


def post_process_output(text):
    """
    Removes special characters, newlines, and extra spaces from a string.
    """
    text = text.replace('\n', ' ')       # new lines
    # text = re.sub(r'[^\w\s]', '', text)  # for special characters
    text = ' '.join(text.split())        # for removing extra spaces
    return text


if __name__ == "__main__":
    api_key = get_api_token()
    print(f"API Key: {api_key}")