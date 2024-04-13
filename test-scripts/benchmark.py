# The MIT License (MIT)
# Copyright © 2023 Rapiiidooo
# Copyright © 2023 Crazydevlegend
# Copyright © 2023 GitPhantomman
# Copyright © 2024 Andrew O'Flaherty
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

#
# Add parent directory '../' to sys.path for benchmarklib. 
# Warning! Maybe collision for 'import compute' module between python sys path 'module/compute' or '../compute' 
#

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(current_dir, '../')
sys.path.append(lib_dir)

#
# Import benchmarklib
#

from benchmarklib.cuda.cuda import *
from benchmarklib.docker.docker import *
from benchmarklib.crypto.hashcat import *
from benchmarklib.crypto.ai_gpu_burn import *

if __name__ == "__main__":
    mode = "hashcat"
    #mode = "gpuburn"
    if mode == 'hashcat':
        miner = Hashcat()
    elif mode == 'gpuburn':
        miner = GpuBurn()
    miner.mine()

