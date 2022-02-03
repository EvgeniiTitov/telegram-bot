.PHONY: help
help:
	@cat $(MAKEFILE_LIST) | grep -e "^[a-zA-Z0-9_\-]*: *.*## *" | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


install:
	pip install --upgrade pip
	pip install -r requirements.txt


pc:
	pre-commit run --all-files


build-docker:
	docker build --build-arg WEATHER_API_KEY=$(WEATHER_API_KEY) \
		   		 --build-arg TELEGRAM_TOKEN=$(TELEGRAM_TOKEN) . \
		   		 -t $(IMAGE_NAME)

run-docker:
	docker run --rm -it -d $(IMAGE_NAME)
