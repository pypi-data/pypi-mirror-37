cmake_minimum_required(VERSION 2.8.12)

project(pygameboycore)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

set(SOURCE_DIR "src/pygameboycore")

add_subdirectory(lib/gameboycore)
add_subdirectory(lib/pybind11)

include_directories(${SOURCE_DIR})
include_directories("lib/gameboycore/include")

pybind11_add_module(pygameboycore ${SOURCES} "${SOURCE_DIR}/bindings.cpp")
target_link_libraries(pygameboycore PRIVATE gameboycore-s)
