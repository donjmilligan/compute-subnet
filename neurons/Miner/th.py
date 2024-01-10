import subprocess
import sys
import json
import os
import string
import secrets
import bittensor as bt
import base64
import random
import rsa

def get_podman_containers():
    # Fetch all Podman containers
    result = subprocess.run(["podman", "ps", "-a", "--format", "json"], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout
    else:
        return None

def kill_podman_container(container_name):
    # Stop and remove a specific Podman container
    result = subprocess.run(["podman", "stop", container_name], capture_output=True, text=True)
    if result.returncode == 0:
        subprocess.run(["podman", "rm", container_name])
        return True
    else:
        return False

def run_podman_container(image_name, container_name, cpu_usage, ram_usage, hard_disk_usage, gpu_usage):
    try:
        password = password_generator(10)
        cpu_assignment = cpu_usage['assignment']
        ram_limit = ram_usage['capacity']
        hard_disk_capacity = hard_disk_usage['capacity']
        gpu_capacity = gpu_usage['capacity']

        # Step 1: Create an SSH server in a container using Podman
        dockerfile_content = f'''
        FROM ubuntu
        RUN apt-get update && apt-get install -y openssh-server
        RUN mkdir -p /run/sshd  # Create the /run/sshd directory
        RUN echo 'root:{password}' | chpasswd
        RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
        RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
        RUN sed -i 's/#ListenAddress 0.0.0.0/ListenAddress 0.0.0.0/' /etc/ssh/sshd_config
        CMD ["/usr/sbin/sshd", "-D"]
        '''

        dockerfile_path = "/tmp/dockerfile"
        with open(dockerfile_path, "w") as dockerfile:
            dockerfile.write(dockerfile_content)

        # Build the image using Podman
        subprocess.run(["podman", "build", "-f", dockerfile_path, "-t", image_name, "."])
    except Exception as e:
        print(f"Error running container: {e}")
        return {'status': False}

def run_container(image_name, container_name, ssh_port, password, public_key):
    try:
        # Run the container using Podman
        subprocess.run([
            "podman", "run", "--name", container_name, "--detach", 
            "-p", f"{ssh_port}:22", image_name
        ])
        
        # Check if the container is created successfully
        container_info = subprocess.run(["podman", "inspect", container_name], capture_output=True)
        container_data = json.loads(container_info.stdout)

        if container_data and container_data[0]["State"]["Status"] == "running":
            info = {'username': 'root', 'password': password, 'port': ssh_port}
            info_str = json.dumps(info)
            public_key = public_key.encode('utf-8')
            encrypted_info = rsa.encrypt_data(public_key, info_str)
            encrypted_info = base64.b64encode(encrypted_info).decode('utf-8')
            return {'status': True, 'info': encrypted_info}
        else:
            return {'status': False}
    except Exception as e:
        print(f"Error running container: {e}")
        return {'status': False}

def check_container(container_name):
    try:
        # Check if the container exists using Podman
        result = subprocess.run(["podman", "inspect", container_name], capture_output=True)
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking container: {e}")
        return False

def set_podman_base_size(base_size):
    try:
        podman_config_file = "/etc/containers/containers.conf"

        # Modify the containers.conf file to set the new base size
        storage_options = f"option_storage_driver = 'devicemapper'\noption_storage_opts = ['dm.basesize={base_size}']"

        with open(podman_config_file, "w") as conf_file:
            conf_file.write(storage_options)

        # Restart Podman service
        subprocess.run(["systemctl", "restart", "podman"])
    except Exception as e:
        print(f"Error setting Podman base size: {e}")

def password_generator(length):
    # Generate a random password
    alphabet = string.ascii_letters + string.digits
    random_str = ''.join(random.choice(alphabet) for _ in range(length))
    return random_str