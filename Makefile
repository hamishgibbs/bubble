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
test: output

output/private/var/folders/m4/w3v2cpxn1x533f4yc3j8_6cm0000gn/T/pytest-of-hamishgibbs/pytest-114/tmp1/src/test.py \ 
	input
test: output

output/private/var/folders/m4/w3v2cpxn1x533f4yc3j8_6cm0000gn/T/pytest-of-hamishgibbs/pytest-115/tmp1/src/test.py \ 
	input
test: output

output/private/var/folders/m4/w3v2cpxn1x533f4yc3j8_6cm0000gn/T/pytest-of-hamishgibbs/pytest-116/tmp1/src/test.py \ 
	input
test: output

output/private/var/folders/m4/w3v2cpxn1x533f4yc3j8_6cm0000gn/T/pytest-of-hamishgibbs/pytest-117/tmp1/src/test.py \ 
	input
test: output

output/private/var/folders/m4/w3v2cpxn1x533f4yc3j8_6cm0000gn/T/pytest-of-hamishgibbs/pytest-118/tmp1/src/test.py \ 
	input
test: output

output/private/var/folders/m4/w3v2cpxn1x533f4yc3j8_6cm0000gn/T/pytest-of-hamishgibbs/pytest-120/tmp1/src/test.py \ 
	input
test: output

output/private/var/folders/m4/w3v2cpxn1x533f4yc3j8_6cm0000gn/T/pytest-of-hamishgibbs/pytest-121/tmp1/src/test.py \ 
	input
test: output

output/private/var/folders/m4/w3v2cpxn1x533f4yc3j8_6cm0000gn/T/pytest-of-hamishgibbs/pytest-122/tmp1/src/test.py \ 
	input
test: output

output/private/var/folders/m4/w3v2cpxn1x533f4yc3j8_6cm0000gn/T/pytest-of-hamishgibbs/pytest-123/tmp1/src/test.py \ 
	input
test: output

output/private/var/folders/m4/w3v2cpxn1x533f4yc3j8_6cm0000gn/T/pytest-of-hamishgibbs/pytest-124/tmp1/src/test.py \ 
	input
test: output

output/private/var/folders/m4/w3v2cpxn1x533f4yc3j8_6cm0000gn/T/pytest-of-hamishgibbs/pytest-130/tmp1/src/test.py \ 
	input
