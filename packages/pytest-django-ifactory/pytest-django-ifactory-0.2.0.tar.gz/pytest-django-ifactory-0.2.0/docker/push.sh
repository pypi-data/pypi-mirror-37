#!/usr/bin/env sh
set -e
BUILD_CONTEXT=`dirname $0`

TARGET=registry.gitlab.com/mjakob422/pytest-django-ifactory/python:2.7
docker build -f $BUILD_CONTEXT/Dockerfile.py2 -t $TARGET $BUILD_CONTEXT
docker push $TARGET

for PYTHON_VERSION in 3.4 3.5 3.6 3.7; do
    TARGET=registry.gitlab.com/mjakob422/pytest-django-ifactory/python:$PYTHON_VERSION
    docker build \
	   --build-arg PYTHON_VERSION=$PYTHON_VERSION \
	   -f $BUILD_CONTEXT/Dockerfile.py3 \
	   -t $TARGET `dirname $0`
    docker push $TARGET
done
