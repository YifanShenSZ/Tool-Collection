cmake_minimum_required(VERSION 3.0 FATAL_ERROR)

project(int2cart)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(CMAKE_BUILD_TYPE Release)

# Foptim
set(CMAKE_PREFIX_PATH ~/Library/Foptim)
find_package(Foptim REQUIRED)

# Torch-Chemistry
set(CMAKE_PREFIX_PATH ~/Library/Torch-Chemistry)
find_package(tchem REQUIRED)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${tchem_CXX_FLAGS}")

add_executable(int2cart.exe int2cart.cpp main.cpp)

target_link_libraries(int2cart.exe ${tchem_LIBRARIES} ${Foptim_LIBRARIES})