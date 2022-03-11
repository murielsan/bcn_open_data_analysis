FROM python:3.10.2

ADD ./ /api

WORKDIR /api

RUN pip install -r requirements.txt

CMD ["uvicorn","main:app"]