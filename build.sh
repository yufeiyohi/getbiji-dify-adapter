#!/bin/bash

unset KUBECONFIG

docker build -f Dockerfile \
             -t yufeiyohi/getbiji-dify-adapter .

docker tag yufeiyohi/getbiji-dify-adapter yufeiyohi/getbiji-dify-adapter:$(date +%y%m%d%H%M)

docker push yufeiyohi/getbiji-dify-adapter:$(date +%y%m%d%H%M)
docker push yufeiyohi/getbiji-dify-adapter:latest