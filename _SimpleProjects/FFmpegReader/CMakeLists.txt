cmake_minimum_required(VERSION 3.0.0)
project(FFMpegReader VERSION 0.1.0)

include(CTest)
enable_testing()

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


set(OpenCV_DIR "/usr/local/opencv_3.4.7/share/OpenCV")
find_package(OpenCV REQUIRED)
if (NOT ${OPENCV_FOUND})
    message(SEND_ERROR "Failed to find OpenCV")
    return()
endif()
list(APPEND LIBRARIES ${OpenCV_LIBS})

find_package(SDL2 REQUIRED)
include_directories(${SDL2_INCLUDE_DIRS})
list(APPEND LIBRARIES ${SDL2_LIBRARIES})


set(FFMPEG_PATH /usr/local/ffmpeg_2.8.1)
set(FFMPEG_LIB_PATH ${FFMPEG_PATH}/lib)
find_library(AVCODEC_LIB avcodec PATHS ${FFMPEG_LIB_PATH} NO_DEFAULT_PATH)
find_library(AVFORMAT_LIB avformat PATHS ${FFMPEG_LIB_PATH} NO_DEFAULT_PATH)
find_library(AVUTIL_LIB avutil PATHS ${FFMPEG_LIB_PATH} NO_DEFAULT_PATH)
find_library(SWSCALE_LIB swscale PATHS ${FFMPEG_LIB_PATH} NO_DEFAULT_PATH)
message(STATUS "FFMPEG_LIB_PATH: ${FFMPEG_LIB_PATH}")
message(STATUS "AVCODEC_LIB: ${AVCODEC_LIB}")
message(STATUS "AVFORMAT_LIB: ${AVFORMAT_LIB}")
message(STATUS "AVUTIL_LIB: ${AVUTIL_LIB}")
message(STATUS "SWSCALE_LIB: ${SWSCALE_LIB}")
if(NOT AVCODEC_LIB OR NOT AVFORMAT_LIB OR NOT AVUTIL_LIB OR NOT SWSCALE_LIB)
    message(FATAL_ERROR "Some of the required ffmpeg components not found")
endif()
include_directories(${FFMPEG_PATH}/include)
link_directories(${FFMPEG_LIB_PATH})
list(APPEND LIBRARIES ${AVCODEC_LIB} ${AVFORMAT_LIB} ${AVUTIL_LIB} ${SWSCALE_LIB})

set ( SOURCES
    main.cpp
    VideoReader/FlowCapture.cpp
)

set ( MOC_HEADERS
    VideoReader/FlowCapture.h
)


add_executable(FFMpegReader ${SOURCES})
target_link_libraries(FFMpegReader ${LIBRARIES})

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
