cmake_minimum_required(VERSION 3.0 FATAL_ERROR)

project(vibration)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(CMAKE_BUILD_TYPE Release)

# Torch-Chemistry
set(CMAKE_PREFIX_PATH ~/Library/Torch-Chemistry)
find_package(tchem REQUIRED)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${tchem_CXX_FLAGS}")

add_executable(vibration.exe main.cpp)

target_link_libraries(vibration.exe ${tchem_LIBRARIES})