cmake_minimum_required(VERSION 2.8)
project(HeaterLauncher)

include_directories(.)

set (CMAKE_CXX_STANDARD 11)

set ( SOURCES
 main.cpp
 ./I2C/TemperatureController.cpp
 MainHeatHandler.cpp
 ./GPIO/GPIOExecuter.cpp
)

include_directories( ${CMAKE_BINARY_DIR} )

add_executable (HeaterLauncher ${SOURCES})

target_link_libraries(HeaterLauncher pthread)
