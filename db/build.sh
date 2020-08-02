#!/bin/bash

docker build -t proj_mysql .
docker tag proj_mysql dlsrks1218/proj_mysql:1.0
docker push dlsrks1218/proj_mysql:1.0
