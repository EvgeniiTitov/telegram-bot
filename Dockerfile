FROM python:3.9-slim-buster as production

ARG WEATHER_API_KEY
ARG TELEGRAM_TOKEN

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV WEATHER_API_KEY=$WEATHER_API_KEY
ENV TELEGRAM_TOKEN=$TELEGRAM_TOKEN

WORKDIR /app
COPY ./requirements.txt .

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

COPY bot ./bot
COPY config.py .

ENTRYPOINT ["python", "-m", "bot"]