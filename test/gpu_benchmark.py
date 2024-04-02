import csv, pathlib, time, numpy as np
from os import getenv
import subprocess

CSV = {}

def benchmark(mnm, nm, fxn):
  tms = []
  for i in range(3):
    print(f"benchmark {mnm} pass {i+1}")
    st = time.perf_counter_ns()
    ret = fxn()
    tms.append(time.perf_counter_ns() - st)
  print(f"{mnm:15s} {nm:25s} {min(tms)*1e-6:7.2f} ms")
  CSV[nm] = min(tms)*1e-6
  return min(tms), ret

def run(cmd):
  try:
    subprocess.run(cmd, shell=True, check=True)
  except subprocess.CalledProcessError as e:
    print(f"Error: {e}")


def benchmark_test_1():
#  benchmark("MOCKUP", f"test_sleep", lambda: {run("./test_sleep_mockup.sh")})
  benchmark("external_model", f"test_tinygrad", lambda: {run("python3 test_modules/tinygrad/test/external/external_model_benchmark.py")})

if __name__ == "__main__":
  benchmark_test_1()
