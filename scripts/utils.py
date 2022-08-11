from pathlib import Path
import requests
from PIL import Image
from io import BytesIO

def format_cost(cost):
    if cost:
        return [{k: v for k, v in mat.items() if k != "type"} for mat in cost]
    return []

def save_image(url, type, id):
    target_path = Path(f"./src/lib/images/{type}/{id}.webp")
    if target_path.is_file():
        pass
    elif (res := requests.get(url)):
        Image.open(BytesIO(res.content)) \
             .convert("RGBA") \
             .save(target_path, "webp")
    else:
        raise RuntimeError(f"Image \"{id}\" of type \"{type}\" could not be retrieved")