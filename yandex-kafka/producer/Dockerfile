FROM python:3.9.8-alpine

COPY requirements.txt .

RUN pip install -U pip && pip install --user -r requirements.txt

WORKDIR /

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]