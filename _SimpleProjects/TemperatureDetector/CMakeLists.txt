cmake_minimum_required(VERSION 3.0.0)
project(VideoTester VERSION 0.1.0)

include(CTest)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON) 
set(OpenCV_DIR "/usr/local/opencv_3.4.7/share/OpenCV")

find_package(OpenCV REQUIRED)

if (NOT ${OPENCV_FOUND})
    message(SEND_ERROR "Failed to find OpenCV")
    return()
endif()

set ( SOURCES
    TemperatureExec/main.cpp
    TemperatureExec/TemperatureCalculator.cpp
)

set ( MOC_HEADERS
    TemperatureExec/TemperatureCalculator.h
)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})

add_executable(VideoTester ${SOURCES})
target_link_libraries(VideoTester ${OpenCV_LIBS})

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
