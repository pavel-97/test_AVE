FROM python:3.12.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

CMD [ "sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload" ]