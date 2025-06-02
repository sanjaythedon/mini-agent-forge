FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN apt-get update \
    && apt-get install -y libpq-dev gcc

RUN pip install -r requirements.txt

EXPOSE 8000

ENV HOST 0.0.0.0

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]