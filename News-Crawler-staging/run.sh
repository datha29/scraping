#!/bin/bash

mkdir -p /usr/src/news/src/logs
touch /usr/src/news/src/logs/crawler_v2.log
gunicorn -w 1 -k uvicorn.workers.UvicornWorker api:app --reload -b 0.0.0.0:9123 --timeout 200
