from fastapi import FastAPI,File, UploadFile , Response
from fastapi.responses import FileResponse , HTMLResponse
import numpy as np 
from PIL import Image, ImageDraw, ImageFont
import torch
import io
from ultralytics import YOLO
import pandas as pd

app = FastAPI()

# model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)
model = YOLO("yolov8n.pt")

def get_bytes_from_image(image: Image) -> bytes:
    return_image = io.BytesIO()
    image.save(return_image, format='JPEG')
    return_image = return_image.getvalue()
    return return_image

def transform_predict_to_df(results: list) -> pd.DataFrame:
    predict_bbox = pd.DataFrame(results[0].to("cpu").numpy().boxes.xyxy, columns=['xmin', 'ymin', 'xmax', 'ymax'])
    predict_bbox['confidence'] = results[0].to("cpu").numpy().boxes.conf
    predict_bbox['class'] = (results[0].to("cpu").numpy().boxes.cls).astype(int)
    return predict_bbox

def draw_bounding_boxes(image: Image.Image, predict_bbox: pd.DataFrame):
    draw = ImageDraw.Draw(image)

    for index, row in predict_bbox.iterrows():
        xmin, ymin, xmax, ymax = row['xmin'], row['ymin'], row['xmax'], row['ymax']
        confidence = row['confidence']
        class_id = row['class']

        draw.rectangle([xmin, ymin, xmax, ymax], outline="green", width=3)

        # label = f"Class: {class_id}, Conf: {confidence:.2f}"
        label = f"Class: {class_id}"
        draw.text((xmin, ymin - 10), label, fill="blue")

    return image

@app.get("/")
async def home():
    return HTMLResponse(content="""
        <html>
        <body>
        <h2>Traffic System With Yolov5</h2>
        <form action="/predict/" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
        </body>
        </html>
    """)


@app.post("/predict/")
async def predict(file: UploadFile):

    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")

    results = model(image)
    pred = transform_predict_to_df(results)
    processed_image = draw_bounding_boxes(image, pred)
    img_byte_array = get_bytes_from_image(processed_image)
    pred_json = pred.to_dict(orient="records")

    # return {"detections": pred_json}
    return Response(content=img_byte_array, media_type="image/jpeg")




