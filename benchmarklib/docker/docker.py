from colorama import Fore, Style
import compute
import docker
import hashlib
from io import BytesIO
import os
import random
import readline
import secrets
import subprocess
import time
from typing import List, Union, Tuple

import bittensor as bt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Docker [

def build_benchmark_container(image_name: str, container_name: str):
    """Create the benchmark container to check Docker's functionality."""

    client = docker.from_env()
    dockerfile = '''
    FROM alpine:latest
    CMD echo "compute-subnet"
    '''
    try:
        # Create a file-like object from the Dockerfile
        f = BytesIO(dockerfile.encode('utf-8'))

        # Build the Docker image
        image, _ = client.images.build(fileobj=f, tag=image_name)

        # Create the container from the built image
        container = client.containers.create(image_name, name=container_name)
        return container
    except docker.errors.BuildError:
        pass
    except docker.errors.APIError:
        pass
    finally:
        client.close()

def check_docker_availability() -> Tuple[bool, str]:
    """Check Docker is available and functioning correctly."""

    try:
        # Run 'docker --version' command
        result = subprocess.run(["docker", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        # If the command was successful, Docker is installed
        docker_version = result.stdout.strip()
        
        if check_docker_container('sn27-benchmark-container') is True:
            return True, docker_version
        else:
            error_message = "Docker is installed, but is unable to create or run a container. Please verify your system's permissions."
            return False, error_message
        
    except Exception as e:  # Catch all exceptions
        # If the command failed, Docker is not installed
        error_message = (
            "Docker is not installed or not found in the system PATH. "
            "Miner initialization has been stopped. Please install Docker and try running the miner again. "
            "Note: running a miner within containerized instances is not supported."
        )
        return False, error_message
    
def check_docker_container(container_id_or_name: str):
    """Confirm the benchmark container can be created and returns the correct output in its logs."""

    try:
        # Start the container
        subprocess.run(["docker", "start", container_id_or_name], 
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)

        # Wait for the container to finish running
        subprocess.run(["docker", "wait", container_id_or_name],
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        
        # Get the logs from the container
        logs_result = subprocess.run(
            ["docker", "logs", container_id_or_name],
            capture_output=True,
            text=True,
            check=True
        )
        output = logs_result.stdout.strip()

        # Check if the output is compute-subnet
        if "compute-subnet" in output:
            return True
        else:
            return False

    except subprocess.CalledProcessError as e:
        # Handle errors from the Docker CLI
        return False
    
# Docker ]