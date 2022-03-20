FROM python:3.10.2

ADD ./ /api

WORKDIR /api

RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=8080

# Command that will start the application
CMD uvicorn main:app --host 0.0.0.0 --port=${PORT}