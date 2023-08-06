ARG PYTHON_VERSION=3.6
FROM python:${PYTHON_VERSION}-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
	libgdal20 \
	libsqlite3-mod-spatialite \
	&& rm -rf /var/lib/apt/lists/*
