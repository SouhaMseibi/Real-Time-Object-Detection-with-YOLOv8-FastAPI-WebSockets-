import asyncio
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import cv2
import threading
from typing import AsyncGenerator
from contextlib import asynccontextmanager
import uvicorn
from typing import Optional, Union
from PIL import Image
from backend.utilities.processing import process_with_yolo , get_bytes_from_image


class Camera:
    """ Handles video capture from the camera. """

    def __init__(self, url: Optional[Union[str, int]] = 0) -> None:
        self.cap = cv2.VideoCapture(url)
        self.lock = threading.Lock()

    def get_frame(self) -> Optional[bytes]:
        """ Captures and processes a frame using YOLO. """
        with self.lock:
            ret, frame = self.cap.read()
            if not ret:
                return None

            # Convert OpenCV BGR image to PIL RGB image
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Process image with YOLO
            processed_image = process_with_yolo(image)

            # Convert to bytes
            return get_bytes_from_image(processed_image)

    def release(self) -> None:
        """ Releases the camera resource. """
        with self.lock:
            if self.cap.isOpened():
                self.cap.release()