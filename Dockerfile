FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3-pip wget unzip curl dpkg git && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

COPY setup.sh /tmp/
RUN chmod +x /tmp/setup.sh && /tmp/setup.sh && rm /tmp/setup.sh

COPY requirements.txt .
RUN pip3 install torch==2.0.0+cu118 torchvision==0.15.1+cu118 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cu118
RUN pip3 install -r requirements.txt