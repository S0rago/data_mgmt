FROM python:3.10-slim-buster

COPY ./requirements.txt /telegram/requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir --upgrade -r /telegram/requirements.txt
COPY . .

CMD ["python", "main.py"]
