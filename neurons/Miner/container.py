# The MIT License (MIT)
# Copyright © 2023 GitPhantomman

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
# Step 1: Import necessary libraries and modules
import subprocess
import json
import string
import secrets
import rsa
import base64
import platform

# Function to install Podman based on the available package manager
def install_podman():
    package_managers = {
        "apt": ["sudo", "apt", "update", "-y", "&&", "sudo", "apt", "install", "-y", "podman"],
        "dnf": ["sudo", "dnf", "install", "-y", "podman"],
        "yum": ["sudo", "yum", "install", "-y", "podman"],
        # Add more package managers and their commands as needed
    }

    system = platform.system()
    try:
        if system == "Linux":
            distro = platform.linux_distribution(full_distribution_name=False)[0].lower()
            for package_manager, command in package_managers.items():
                if subprocess.run(["which", package_manager], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                    print(f"Using {package_manager} to install Podman...")
                    subprocess.run(command)
                    return True
            print("No compatible package manager found to install Podman.")
            return False
        else:
            print("Podman installation is only supported on Linux systems.")
            return False
    except Exception as e:
        print(f"Error installing Podman: {e}")
        return False

# Check if Podman is installed, and install it if necessary
if not subprocess.run(["which", "podman"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
    if not install_podman():
        exit("Podman installation failed. Exiting...")

# Function to generate a random password
def password_generator(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

# Function to generate a random name
def generate_random_name(prefix):
    return f"{prefix}_{secrets.token_hex(4)}"

# Function to retrieve Podman containers
def get_podman_containers():
    try:
        result = subprocess.run(["sudo", "podman", "ps", "-a", "--format", "json"], stdout=subprocess.PIPE, universal_newlines=True, check=True)
        containers = json.loads(result.stdout)
        return containers
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving containers: {e}")
        return []

# Function to stop and remove Podman containers
def stop_and_remove_containers():
    containers = get_podman_containers()

    for container in containers:
        container_id = container['ID']
        print(f"Stopping container {container_id}")
        stop_podman_container(container_id)

        print(f"Removing container {container_id}")
        remove_podman_container(container_id)

def stop_podman_container(container_id):
    try:
        subprocess.run(["sudo", "podman", "stop", container_id], check=True)
        print(f"Container {container_id} stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error stopping container {container_id}: {e}")

def remove_podman_container(container_id):
    try:
        subprocess.run(["sudo", "podman", "rm", container_id], check=True)
        print(f"Container {container_id} removed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error removing container {container_id}: {e}")

# Function to run a Podman container
def run_podman_container():
    try:
        # Generate unique names for image and container
        image_name = generate_random_name("my_image")
        container_name = generate_random_name("my_container")

        password = password_generator(10)

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

        # Step 2: Build the image using Podman
        build_command = ["sudo", "podman", "build", "-f", dockerfile_path, "-t", image_name, "."]
        subprocess.run(build_command, check=True)

        # Step 3: Return the image and container names for future reference
        return {'image_name': image_name, 'container_name': container_name, 'status': True, 'password': password}
    except Exception as e:
        print(f"Error running container: {e}")
        return {'status': False}

# Function to run a Podman container with encryption
def run_container(image_name, container_name, ssh_port, password):
    try:
        # Run the container using Podman
        subprocess.run([
            "sudo", "podman", "run", "--name", container_name, "--detach", 
            "-p", f"{ssh_port}:22", image_name
        ])
        
        # Check if the container is created successfully
        container_info = subprocess.run(["sudo", "podman", "inspect", container_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        container_data = json.loads(container_info.stdout.decode('utf-8'))

        if container_data and container_data[0]["State"]["Status"] == "running":
            info = {'username': 'root', 'password': password, 'port': ssh_port}
            return {'status': True, 'info': info, 'image_name': image_name}
        else:
            return {'status': False}
    except Exception as e:
        print(f"Error running container: {e}")
        return {'status': False}

# Function to encrypt data using RSA
def encrypt_rsa(public_key, data):
    try:
        key = rsa.PublicKey.load_pkcs1(public_key)
        encrypted_data = rsa.encrypt(data.encode('utf-8'), key)
        return encrypted_data
    except Exception as e:
        print(f"Error encrypting data: {e}")
        return None

# Function to check if a container exists using Podman
def check_container(container_name):
    try:
        result = subprocess.run(["sudo", "podman", "inspect", container_name], capture_output=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error checking container: {e}")
        return False

# Function to set Podman base size
def set_podman_base_size(base_size):
    try:
        podman_config_file = "/etc/containers/containers.conf"

        # Modify the containers.conf file to set the new base size
        storage_options = f"option_storage_driver = 'devicemapper'\noption_storage_opts = ['dm.basesize={base_size}']"

        with open(podman_config_file, "w") as conf_file:
            conf_file.write(storage_options)

        # Restart Podman service
        subprocess.run(["sudo", "systemctl", "restart", "podman"])
    except Exception as e:
        print(f"Error setting Podman base size: {e}")

# Function to generate a random password
def password_generator(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

# Function to generate a random name
def generate_random_name(prefix):
    return f"{prefix}_{secrets.token_hex(4)}"

# Usage example:
# Check if Podman is installed, and install it if necessary
if not subprocess.run(["which", "podman"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
    if not install_podman():
        exit("Podman installation failed. Exiting...")

# Get Podman containers and display them
containers = get_podman_containers()
if containers:
    print(containers)

# Stop and remove Podman containers
stop_and_remove_containers()

# Run a new container
container_info = run_podman_container()
if container_info['status']:
    print(f"Image Name: {container_info['image_name']}")
    print(f"Container Name: {container_info['container_name']}")
    print(f"Password: {container_info['password']}")
else:
    print("Failed to run container.")

# Run a new container with encryption
public_key, private_key = rsa.newkeys(2048)
container_info_encrypted = run_container(container_info['image_name'], container_info['container_name'], "2222", container_info['password'])
if container_info_encrypted['status']:
    encrypted_info = rsa.encrypt(json.dumps(container_info_encrypted['info']).encode('utf-8'), public_key)
    if encrypted_info:
        print(f"Encrypted Info: {base64.b64encode(encrypted_info).decode('utf-8')}")
else:
    print("Failed to run container with encryption.")
