cmake_minimum_required(VERSION 3.20)
project (miniapp CUDA CXX)

include (GNUInstallDirs)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR}")

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(OpenMP)

add_executable(miniapp "")
target_sources(miniapp
  PRIVATE
    stats.cu
    data.cu
    operators.cu
    linalg.cu
    main.cu
)
set_target_properties(miniapp PROPERTIES CUDA_ARCHITECTURES "86")

set(INSITU None CACHE STRING "Enable in-situ support")
set_property(CACHE INSITU PROPERTY STRINGS None Catalyst Ascent VTK-m Viskores)

if(INSITU STREQUAL "None")
  target_link_libraries(miniapp PRIVATE OpenMP::OpenMP_CXX cublas cudart)
elseif(INSITU STREQUAL "Catalyst")
  find_package(catalyst REQUIRED PATHS "${EBROOTCATALYST}/lib/cmake/catalyst-2.0")
  target_compile_definitions(miniapp PUBLIC USE_CATALYST=1)
  target_link_libraries(miniapp PRIVATE OpenMP::OpenMP_CXX cublas cudart catalyst::catalyst)
endif()
