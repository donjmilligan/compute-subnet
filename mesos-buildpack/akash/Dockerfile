FROM debian:bullseye-slim as blockchain 
ENV DEBIAN_FRONTEND noninteractive
# Environment variables for CUDA setup

# Install necessary packages
RUN apt update && \
    apt install -y \
    git \
    curl \
    python3-pip \
    wget \
    make \
    ca-certificates \
    dpkg && \
    rm -rf /var/lib/apt/lists/*

RUN apt update && \
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg &&\
    curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    tee /etc/apt/sources.list.d/nvidia-container-toolkit.list && \
    apt update && \
    apt install -y nvidia-container-toolkit 

# Clone the repository and install Python dependencies
RUN git clone https://github.com/neuralinternet/Compute-Subnet.git && \
    cd Compute-Subnet && \
    python3 -m pip install --no-cache-dir -U pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt && \
    python3 -m pip install --no-cache-dir -e .

RUN apt update && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian\
        $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
        tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt update -y && \
    apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin && \
    systemctl start docker

# Download, extract, and install Hashcat
RUN wget https://hashcat.net/files/hashcat-6.2.6.tar.gz && \
    tar xzvf hashcat-6.2.6.tar.gz && \
    cd hashcat-6.2.6/ && \
    make && \
    make install && \
    hashcat --version && \
    cd .. && rm -rf hashcat-6.2.6 hashcat-6.2.6.tar.gz

WORKDIR /Compute-Subnet/neurons/

FROM blockchain as miner
ENTRYPOINT [ "./miner" ]

FROM blockchain as validator
ENTRYPOINT [ "./validator" ]
