from fastapi import APIRouter, UploadFile, Response , File , BackgroundTasks
from PIL import Image
import io
from backend.utilities.processing import get_bytes_from_image, transform_predict_to_df, draw_bounding_boxes
from backend.models.yolo_model import run_yolo


router = APIRouter()

@router.post("/predict/")
async def predict(file: UploadFile):
    
    image_data = await file.read()

    image = Image.open(io.BytesIO(image_data)).convert("RGB")

    results = run_yolo(image)

    pred = transform_predict_to_df(results)

    processed_image = draw_bounding_boxes(image, pred)
   
    img_byte_array = get_bytes_from_image(processed_image)

    return Response(content=img_byte_array, media_type="image/jpeg")


