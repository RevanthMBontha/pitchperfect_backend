import cv2
import os
import math
import requests
import numpy as np
import sys
import time
import json

def resize_to_aspect(image, target_width, target_height):
    h, w = image.shape[:2]
    target_aspect = target_width / target_height
    image_aspect = w / h

    if image_aspect > target_aspect:
        new_width = target_width
        new_height = int(target_width / image_aspect)
    else:
        new_height = target_height
        new_width = int(target_height * image_aspect)

    resized = cv2.resize(image, (new_width, new_height))

    result = np.zeros((target_height, target_width, 3), dtype=np.uint8)

    x_offset = (target_width - new_width) // 2
    y_offset = (target_height - new_height) // 2

    result[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = resized

    return result

def download_image(url):
    """
    Downloads an image from a given URL and returns the image data.
    
    Args:
        url (str): The URL of the image to download.
        
    Returns:
        bytes: The image data if successful, None otherwise.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            image_array = np.frombuffer(response.content, np.uint8)
            image_cv2 = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            return image_cv2
        else:
            print(f"Failed to download image from {url}, status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception encountered while downloading image from {url} - {e}")
        return None

def generate_video_from_images(image_urls, orientation, audio_duration):
    """
    Generates a video from a sequence of images in a specified folder.
    The images should be named in a way that they can be sorted correctly (e.g., img1.jpg, img2.jpg).
    """

    fps = 25
    output_video_path = f"{int(time.time())}.mp4"

    audio_duration = int(float(audio_duration))

    min_length = min(len(image_urls), 6)
    image_count = math.ceil(audio_duration/min_length)
    
    if orientation == "portrait":
        height, width, _ = (640, 360, 3)
    else:
        height, width, _ = (360, 640, 3)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(f"public/videos/{output_video_path}", fourcc, fps, (width, height))
    
    count = 0
    max_frame_count = audio_duration * fps
    
    for i in range(min_length):
        url = image_urls[i]
        image = download_image(url)

        if count >= max_frame_count:
            break
        for j in range(fps*image_count):
            count+=1
            if image is None:
                continue
            
            if count > max_frame_count:
                break
        
            image_resized = resize_to_aspect(image, width, height)
            video_writer.write(image_resized)
    # Release the video writer
    video_writer.release()
    return output_video_path

if __name__ == "__main__":
    images, orientation, audio_duration = sys.argv[1:4]
    images = json.loads(images)
    outputPath = generate_video_from_images(images, orientation, audio_duration)
    print(outputPath)