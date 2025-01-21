import requests
from PIL import Image
import io

image_path = "/home/souha/traffic/img.jpg"
url = "http://127.0.0.1:8000/predict/"

with open(image_path, "rb") as img:
    response = requests.post(url, files={"file": img})

# print(response.json())


if response.status_code == 200:

    image_bytes = io.BytesIO(response.content)
    image = Image.open(image_bytes)
    image.show()
   
else:
    print("Error:", response.text)
