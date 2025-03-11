# Real-Time Object Detection with YOLOv8 (FastAPI + WebSockets)

This project provides **real-time object detection** using **YOLOv8** with **FastAPI**, WebSockets for:
- **Uploading and processing images**.
- **Capturing snapshots from local camera**.
- **Live video streaming from local camera**.

![Image](https://github.com/user-attachments/assets/39aba110-99c4-49e6-86f6-e20c0fcf361c)

### Set up the camera based on your source:
#### Default Local Webcam
```bash
python3 main.py -c 0
```


#### USB Camera
Check available devices:
```bash
cd /dev && ls | grep video
```
Then use the appropriate video source, example:
```bash
python3 main.py -c /dev/video0
```
#### IP Camera
You can pass the rtsp url of IP camera stream:
```bash
python3 main.py -c rtsp://user:password@ip_address:port/
```
Or you access a IP camera and convert it to /dev/video using ffmpeg:
```bash
ffmpeg -i rtsp://user:password@ip_address:port/ -f v4l2 -pix_fmt yuv420p /dev/video1
```
Then 
```bash
python3 main.py -c /dev/video1
```

### Change the YOLO version
You can edit the file **backend/models/yolo_model.py** to use a different YOLO version 

###  **Build the Docker Image**
Make sure you are in the root directory of the project.
If a webcam is used, then run:

```bash
docker build -t fastapi-yolo .

docker run -p 8000:8000 --device /dev/video0 devfastapi-yolo
```
If an usb camera is used, check available devices in **/dev/video** like the previous steps, change the **-c** of camera device in Dockerfile, build the image and run it with the updated **--device** path to the camera file.

If an IP camera is used , convert it to **/dev/video** using ffmpeg, then do the same steps as usb camera.
