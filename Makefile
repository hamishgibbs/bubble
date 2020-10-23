# Search for .env file variables
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

#Build a new docker image
build:
	docker build -t bubble .

#Run image bash
bash:
	docker run -it --rm --mount type=bind,source="${PWD}",target=/usr/bubble/ bubble bash
