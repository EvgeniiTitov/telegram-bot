import os


class Config:
    _TOKEN = os.environ.get("TELEGRAM_TOKEN")
    _WEATHER_KEY = os.environ.get("WEATHER_API_KEY")

    EUGENE_CHAT_ID = 378612721
    WEATHER_URL = "http://api.weatherapi.com/v1/current.json?key={key}&q={loc}"
    ENGLISH_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    CRYPTO_URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}&ids={coin}"

    TEST_URLS = [
        "https://api.agify.io?name={name}",
        "https://api.genderize.io?name={name}",
        "https://api.nationalize.io?name={name}",
    ]

    @staticmethod
    def telegram_token() -> str:
        if not Config._TOKEN:
            raise EnvironmentError("Provide TELEGRAM_TOKEN env variable")
        return Config._TOKEN

    @staticmethod
    def weather_api_key() -> str:
        if not Config._WEATHER_KEY:
            raise EnvironmentError("Provide WEATHER_API_KEY env variable")
        return Config._WEATHER_KEY
