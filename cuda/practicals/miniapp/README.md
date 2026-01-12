# mini-app instrumented to do in-situ visualization

### Compilation

Minimal CMake configuration:
```shell
cmake -S . -B build
cmake --build build

uenv start prgenv-gnu/25.6:v1 --view=spack
export SPACK_SYSTEM_CONFIG_PATH="/user-environment/config"
spack load cray-mpich@8.1.32 cmake cuda@12.9.0/xo libcatalyst

cmake -S . -B buildCatalyst -DINSITU=Catalyst
cmake --build buildCatalyst

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:`spack location -i cuda@12.9.0/xo`/lib64
export CATALYST_IMPLEMENTATION_PATHS=/capstor/scratch/cscs/jfavre/ParaView/dev/lib64/catalyst
srun -t5 -pnormal --gpus-per-task=1 -n1 -N1 /users/jfavre/Projects/ParaView/select_local_device.sh buildCatalyst/bin/miniapp 256 256 1000 .01 0 ../catalyst_pipeline.py
```

