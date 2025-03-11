
FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y python3-opencv \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir opencv-python \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000


CMD ["python3", "main.py" , "-c /dev/video0" ]
# CMD ["fastapi" , " run" , "main.py"]