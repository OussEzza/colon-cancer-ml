FROM python:3.11-slim

WORKDIR /training

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY data/ ./data/
COPY train.py .

CMD ["python", "train.py"]