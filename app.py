from fastapi import FastAPI,File, UploadFile , Response
from fastapi.responses import FileResponse , HTMLResponse
import numpy as np 
from PIL import Image, ImageDraw, ImageFont
import torch
import io
from ultralytics import YOLO
import pandas as pd

app = FastAPI()

# model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/souha/traffic/best.pt', force_reload=True)
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
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>YOLO Object Detection</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: #f4f4f4;
                    text-align: center;
                    margin: 50px;
                }
                h2 {
                    color: #333;
                }
                .upload-container {
                    background: #fff;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    max-width: 500px;
                    margin: auto;
                }
                input[type="file"] {
                    display: none;
                }
                .custom-file-upload {
                    display: inline-block;
                    padding: 10px 20px;
                    cursor: pointer;
                    background: #28a745;
                    color: #fff;
                    border-radius: 5px;
                    font-size: 16px;
                }
                .custom-file-upload:hover {
                    background: #218838;
                }
                button {
                    background: #007bff;
                    border: none;
                    color: white;
                    padding: 15px 20px;
                    cursor: pointer;
                    font-size: 16px;
                    border-radius: 5px;
                }
                button:hover {
                    background: #0056b3;
                }
                #output-img {
                    margin-top: 20px;
                    max-width: 100%;
                    border-radius: 10px;
                    display: none;
                    border: 2px solid #333;
                }
            </style>
        </head>
        <body>
            <h2>Upload an Image for YOLO Detection</h2>
            <div class="upload-container">
                <form id="upload-form">
                    <label for="file-upload" class="custom-file-upload">
                        Choose File
                    </label>
                    <input id="file-upload" type="file" name="file" onchange="displayFileName()">
                    <p id="file-name">No file selected</p>
                    <br><br>
                    <button type="submit">Upload and Process</button>
                </form>
            </div>

            <img id="output-img" src="" alt="Processed Image">
            
            <script>
                function displayFileName() {
                    var input = document.getElementById('file-upload');
                    var fileName = document.getElementById('file-name');
                    fileName.textContent = input.files[0].name;
                }

                document.getElementById("upload-form").onsubmit = async function(e) {
                    e.preventDefault();
                    let formData = new FormData();
                    let fileInput = document.getElementById("file-upload");
                    formData.append("file", fileInput.files[0]);

                    let response = await fetch("/predict/", {
                        method: "POST",
                        body: formData
                    });

                    if (response.ok) {
                        let imageBlob = await response.blob();
                        let imageUrl = URL.createObjectURL(imageBlob);
                        document.getElementById("output-img").src = imageUrl;
                        document.getElementById("output-img").style.display = "block";
                    } else {
                        alert("Error processing the image.");
                    }
                };
            </script>
        </body>
        </html>
    """)


@app.post("/predict/")
async def predict(file: UploadFile):

    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")

    results = model(image)
    print(results)
    pred = transform_predict_to_df(results)
    processed_image = draw_bounding_boxes(image, pred)
    img_byte_array = get_bytes_from_image(processed_image)
    pred_json = pred.to_dict(orient="records")

    # return {"detections": pred_json}
    return Response(content=img_byte_array, media_type="image/jpeg")




