FROM python:3.12-slim
RUN apt-get update && apt-get upgrade -y
RUN apt-get install git curl libboost-tools-dev libboost-dev libboost-system-dev libboost-all-dev gcc make build-essential libssl-dev -y
RUN python -m pip install wheel setuptools
WORKDIR /app
RUN git clone --recurse-submodules https://github.com/arvidn/libtorrent.git --depth=1
WORKDIR /app/libtorrent
RUN python setup.py bdist_wheel
