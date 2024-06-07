# FAQ

# WanDB 

## How do miner and validator defend against malicious peers?
Miner and validator runs are signed with a signature, it’s not possible to fake information (e.g. allocation status) if your not the creator of the run.
If that were possible, there would have been miners who would have taken advantage of it long ago 


# Code

## Issue: Benchmark checking container crash

Issue: Benchmark checking container crash

Path: test-scripts/benchmark.py

Description: Crash at astartup without docker

Solution: Disable checking container

Todo: Add option
```
#    build_benchmark_container('compute-subnet-benchmark','sn27-benchmark-container')
```
https://github.com/xen1024/compute-subnet/commit/570e97d4471a484def119710ab83836c86c48f3d

## ❌ Hashcat execution timed out 

```
5HbLYXUB/11/9d95cc9783: ♻️  Challenge processing
hashcat '$BLAKE2$639d95cc9783fcb35993ca82f8ef861bf197b9f4e47bab5af94c7d912292661e04fa719d6eae6aff06770a61020e469927bb9719a014548fc04519093b5ee85b:f68f8566a8c96725' -a 3 -D 2 -m 610 -1 '>0@&e$,2iM' '?1?1?1?1?1?1?1?1?1?1?1' -w 3 ''
Block: 3125863 | Stake: 0.0000 | Trust: 0.0000 | Consensus: 0.000000 | Incentive: 0.000000 | Emission: 0.000000 | update_validator: #3125865 ~ 0:00:24 | sync_status: #3125885 ~ 0:04:24
wandb: 429 encountered (Filestream rate limit exceeded, retrying in 2.2 seconds.), retrying request
wandb: 429 encountered (Filestream rate limit exceeded, retrying in 4.6 seconds.), retrying request
Block: 3125864 | Stake: 0.0000 | Trust: 0.0000 | Consensus: 0.000000 | Incentive: 0.000000 | Emission: 0.000000 | update_validator: #3125865 ~ 0:00:12 | sync_status: #3125885 ~ 0:04:12
2024-06-07 10:07:27.294 |     WARNING      | bittensor:loggingmachine.py:289 |  - 5HbLYXUB/11/9d95cc9783: ❌ Hashcat execution timed out -
```

This is by design and expected

Well this is exactly what is happening. The hashcat execution times out. This will negatively affect the miners score. It’s imperative the user sees these errors so they can correct it.

And yes it is normally due to you not solving within the set time frame. This usually directly correlates to the miners compute power.

More compute power = quicker solutions. Less = slower.











