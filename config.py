import os


class Config:
    _TOKEN = os.environ.get("TELEGRAM_TOKEN")

    @property
    def token(self) -> str:
        if not Config._TOKEN:
            raise EnvironmentError("Provide TELEGRAM_TOKEN env variable")
        return Config._TOKEN
