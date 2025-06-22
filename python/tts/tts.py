import requests
import time
import sys
import os

def get_voice_from_script(script, voice, openai_api_key, filename=int(time.time())):
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "tts-1",
        "input": script,
        "voice": voice
    }

    response = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers=headers,
        json=data
    )
    if response.status_code == 200:
        with open(f"{os.getcwd()}/public/audios/{filename}.mp3", "wb") as f:
            f.write(response.content)
            return f"{filename}.mp3"
    return False


if __name__ == "__main__":
    script = sys.argv[1]
    voice = sys.argv[2]
    openai_api_key = sys.argv[3]
    output = get_voice_from_script(script, voice, openai_api_key)
    print(output)