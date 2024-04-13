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

# Cuda [

def check_cuda_availability():
    """Verify the number of available CUDA devices (Nvidia GPUs)"""

    import torch

    if torch.cuda.is_available():
        device_count = torch.cuda.device_count()
        print(Fore.GREEN + f"CUDA is available with {device_count} CUDA device(s)!")
    else:
        print(Fore.RED + "CUDA is not available or not properly configured on this system.")

# Cuda ]
