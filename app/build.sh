#!/bin/bash

docker build -t proj_python .
docker tag proj_python dlsrks1218/proj_python:1.0
docker push dlsrks1218/proj_python:1.0
