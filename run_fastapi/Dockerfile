FROM python:3.8-slim-buster

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install -r requirements.txt

CMD exec uvicorn main:app --reload --host 0.0.0.0 --port $PORT

