import io
import pandas as pd
from PIL import Image, ImageDraw
from backend.models.yolo_model import run_yolo


def get_bytes_from_image(image: Image.Image) -> bytes:
    return_image = io.BytesIO()
    image.save(return_image, format='JPEG')
    return return_image.getvalue()

def transform_predict_to_df(results: list) -> pd.DataFrame:
    predict_bbox = pd.DataFrame(results[0].to("cpu").numpy().boxes.xyxy, columns=['xmin', 'ymin', 'xmax', 'ymax'])
    predict_bbox['confidence'] = results[0].to("cpu").numpy().boxes.conf
    predict_bbox['class'] = (results[0].to("cpu").numpy().boxes.cls).astype(int)
    return predict_bbox

def draw_bounding_boxes(image: Image.Image, predict_bbox: pd.DataFrame):
    draw = ImageDraw.Draw(image)
    for _, row in predict_bbox.iterrows():
        draw.rectangle([row['xmin'], row['ymin'], row['xmax'], row['ymax']], outline="green", width=3)
    return image

def process_with_yolo(image: Image.Image) -> Image.Image:
    """ Runs YOLO model on an image and draws bounding boxes. """
    results = run_yolo(image)
    pred = transform_predict_to_df(results)
    return draw_bounding_boxes(image, pred)

