## Compute Subnet Docker in Docker alternative + Runpod fix  

This project integrates Apache Mesos with PySpark to orchestrate jobs using pre-existing Python scripts. It addresses compatibility issues with RunPod environments by employing a multi-stage Docker build, enabling different isolation configurations: one with cgroups and POSIX for general use, and another with just POSIX for RunPod due to its SELinux restrictions on cgroup manipulation.

### Additional Dependencies
#### Host OS
Apache Mesos
#### Project requirements.txt
PySpark
