#!/bin/bash
docker build -t webapp web-server
docker run --rm --network Internal --ip 10.0.0.10 --name web-server webapp