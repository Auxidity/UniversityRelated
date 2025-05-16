# File : Dockerfile
# Author : Daniel Kortesmaa
# Description : Dockerfile for creating a server container

# Use an official Python 3 image as a parent image
FROM python:3


# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    x11-apps\
    bison \
    swig \
    python3 \
    python3-dev \
    libportaudio2 \
    libportaudiocpp0 \
    portaudio19-dev \
    python3-tk \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    python3-openssl \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*



# Install pyenv
RUN curl https://pyenv.run | bash

# Set environment variables for pyenv
ENV PATH="/root/.pyenv/bin:$PATH"
RUN echo 'eval "$(pyenv init --path)"' >> ~/.bashrc

# Install Python 2 using pyenv
RUN pyenv install 2.7.18
RUN pyenv global 2.7.18
# Set the path to Python 2
RUN ln -s /root/.pyenv/versions/2.7.18/bin/python /usr/local/bin/python2
#Install Python 3 and set it as global
RUN pyenv install 3.8.12
RUN pyenv global 3.8.12

# Copy everything inside Backend
COPY scripts/Backend/ /app/scripts

# Copy SDK files into the container
COPY Lib/pynaoqi-python2.7-2.5.5.5-linux64 /app/sdk/


# Install any needed Python packages specified in requirements.txt using pip3
RUN pip3 install --no-cache-dir -r scripts/requirements.txt

# Set Python version to 3
RUN pyenv global system

# Set environment variable for SDK path
ENV PYTHONPATH=/app/sdk/lib/python2.7/site-packages

# Run the Python script when the container launches
CMD ["python3", "/app/scripts/main.py"]
