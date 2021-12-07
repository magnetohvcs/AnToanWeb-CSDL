#!/bin/bash
docker network create --driver=bridge --subnet=10.0.0.0/8 --gateway=10.0.0.1 Internal