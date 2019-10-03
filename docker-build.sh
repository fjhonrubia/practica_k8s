#!/bin/bash

docker build -t eu.gcr.io/pmoncada-001/keepcoding/flask-counter:v1.3.0 .
docker push eu.gcr.io/pmoncada-001/keepcoding/flask-counter:v1.3.0