cmake_minimum_required(VERSION 3.0 FATAL_ERROR)

project(translate_IntCoordDef)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(CMAKE_BUILD_TYPE Release)

# Torch-Chemistry
set(CMAKE_PREFIX_PATH ~/Library/Torch-Chemistry)
find_package(tchem REQUIRED)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${tchem_CXX_FLAGS}")

add_executable(translate_IntCoordDef.exe main.cpp)

target_link_libraries(translate_IntCoordDef.exe ${tchem_LIBRARIES})