
FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python

EXPOSE 8000

CMD ["fastapi", "run", "main.py" ]
