#/bin/bash

docker run --network host --rm --name wish-lists -v $PWD:/code wish-lists:latest
