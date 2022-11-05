try:
    import openai
except ImportError as err:
    print("Install openai")
    print(err.msg)
    exit()

import os
import requests
import sys

def _get_env_data_as_dict(path: str) -> dict:
    with open(path, 'r') as f:
       return dict(tuple(line.replace('\n', '').split('=')) for line
                in f.readlines() if not line.startswith('#'))


OPENAI_API_KEY = _get_env_data_as_dict(".env")["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY
IMG_COUNTER = 0

def generate_image(prompt: str, size: str = "256x256", n:int = 1) -> dict:
    if (size not in ['256x256', '512x512', '1024x1024']):
        print("Size must be either 256x256, 512x512, or 1024x1024")
        return None

    response = openai.Image.create(
        prompt=prompt,
        n=n,
        size=size
    )
    return response

def extract_image_url(data: dict) -> str:
    if len(data["data"]) == 1:
        return data["data"][0]["url"]
    else:
        return [url["url"] for url in data["data"]]

def _download_single_image(image_url: str, to: str = "."):
    """
    Downloads a single image from url into the directory to.

    Params:
    image_url: the url of the image
    to: the directory that the images is going to be saved to

    Returns:
    None
    """
    img_data = requests.get(image_url).content
    if (to == ""):
        global IMG_COUNTER
        with open(f'img{IMG_COUNTER}.jpg', 'wb') as handler:
            handler.write(img_data)
            IMG_COUNTER += 1
    else:
        with open(f'{to}/img{IMG_COUNTER}.jpg', 'wb') as handler:
            handler.write(img_data)
            IMG_COUNTER += 1

def download_image_from(image_urls: list, to: str = "."):
    """
    Downloads the images from the urls given in a list to the directory given by to.

    Params:
    image_urls: a list containing the generated image URLs 
    to: the directory that the images is going to be saved to

    Returns:
    None
    """

    if (not os.path.isdir(to)):
        os.makedirs(to)

    for url in image_urls:
        _download_single_image(url, to)
    

if __name__ == "__main__":
    "python dalle.py <prompt> <size> <n> <to>"

    prompt = sys.argv[1]
    size = sys.argv[2]
    n = int(sys.argv[3])
    to =  sys.argv[4] if len(sys.argv) == 5  else "."
    download_image_from(extract_image_url(generate_image(prompt, size = size, n = n)), to=to)
