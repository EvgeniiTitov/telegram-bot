#### I am genuinely bored


To remember:

1) This will map XXX to args in dockerfile so they become ENV when running the container

```
docker build --build-arg WEATHER_API_KEY=XXX --build-arg TELEGRAM_TOKEN=XXX . -t tele-bot-v2
```

