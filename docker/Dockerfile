# syntax=docker/dockerfile:1

FROM continuumio/miniconda3:4.10.3p0-alpine AS miniconda

FROM nvidia/cuda:10.1-cudnn8-devel-ubuntu18.04 AS main

# Set up CUDA build machine
ENV DEBIAN_FRONTEND noninteractive
ENV HOME_PATH=/home
ENV PROJ_PATH=${HOME_PATH}/FGVC

# We just need conda from the alpine miniconda build

COPY --from=miniconda /opt/conda /opt/conda

RUN echo "export PATH=\${PATH}:/opt/conda/bin" >> ~/.bashrc
ENV PATH=${PATH}:/opt/conda/bin

# Install apt dependencies first

RUN apt-get update && \
    apt-get install -y \
        git \
        libsm6 \
        libxext6 \
        rsync \
        unzip \
        wget

# Create conda env

RUN conda create -n fgvc

# activate conda env and add to .bashrc

SHELL ["conda", "run", "-n", "fgvc", "/bin/bash", "-c"]
RUN echo "source activate fgvc" >> ~/.bashrc

# install conda dependencies

RUN conda install -y \
        -c pytorch \
        pytorch=1.6.0 \
        torchvision=0.7.0 \
        cudatoolkit=10.1 \
        matplotlib \
        scipy \
        opencv \
        x264 \
        ffmpeg

# install pip dependencies

RUN pip install \
        imageio \
        imageio-ffmpeg \
        scikit-image \
        imutils

# Clone github repo

RUN git clone https://github.com/JamesPerlman/FGVC.git ${PROJ_PATH} && \
    echo Cache busting... cloning commit e91a3f

WORKDIR ${PROJ_PATH}

# Download model weights

RUN chmod +x download_data_weights.sh && \
    ./download_data_weights.sh
