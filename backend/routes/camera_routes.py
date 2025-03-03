import asyncio
from fastapi import APIRouter, Response, WebSocket , WebSocketDisconnect
from backend.utilities.processing import get_bytes_from_image, transform_predict_to_df, draw_bounding_boxes
from backend.models.yolo_model import run_yolo
from backend.utilities.camera_class import Camera

router = APIRouter()
camera = Camera()  

@router.get("/snapshot")
async def snapshot():
    """Captures a single YOLO-processed frame and returns it."""
    frame = camera.get_frame()
    if frame:
        return Response(content=frame, media_type="image/jpeg")
    return Response(status_code=404, content="Camera frame not available.")


@router.websocket("/video")
async def video_stream(websocket: WebSocket):
    """WebSocket endpoint that streams YOLO-processed frames."""
    await websocket.accept()
    try:
        while True:
            frame = camera.get_frame()
            if frame:
                await websocket.send_bytes(frame)
            await asyncio.sleep(0.1)  # Control the frame rate
    except WebSocketDisconnect:
        print("WebSocket connection closed by client.")
    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        try:
            await websocket.close()
        except RuntimeError:
            print("WebSocket was already closed.")


