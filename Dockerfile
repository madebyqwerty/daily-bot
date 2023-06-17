FROM python:3.11.3-alpine

WORKDIR /app

RUN apk update

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]