FROM python:3.10-slim

WORKDIR /app

COPY ml-pipeline/model_training/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ml-pipeline/model_training /app

ENTRYPOINT ["python", "train.py"]