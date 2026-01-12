# mini-app instrumented to do in-situ visualization

### Compilation

Minimal CMake configuration:
```shell
cmake -S . -B build
cmake --build build
cmake -S . -B buildCatalyst -DINSITU=Catalyst
cmake --build buildCatalyst
```

