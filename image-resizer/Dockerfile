FROM python:3.10-slim-buster

COPY requirements.txt .

RUN apt update
RUN apt install ffmpeg libsm6 libxext6  -y
RUN pip install -U pip && pip install --user -r requirements.txt

WORKDIR /

COPY . .

CMD ["python", "main.py"]
