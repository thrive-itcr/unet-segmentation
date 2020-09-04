#!/bin/bash
# Copyright (c) General Electric Company, 2017.  All rights reserved.

echo ""
echo "Removing algorithm image."
docker rmi thriveitcr/rt106-algorithm-sdk

echo ""
echo "Building algorithm image."
docker build -t thriveitcr/rt106-algorithm-sdk --build-arg http_proxy=$http_proxy --build-arg https_proxy=$https_proxy .

echo ""
docker images
