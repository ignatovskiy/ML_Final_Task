FROM python:3.11-buster
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD uvicorn fastapi_server:app --reload --host 0.0.0.0 --port 8000