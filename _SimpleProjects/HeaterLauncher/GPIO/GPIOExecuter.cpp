/* 
 * File:   GPIOExecuter.cpp
 * Author: Ilya Petrikov
 * 
 * Created on January 30, 2020, 12:55 PM
 */


#include <iostream>

#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "GPIOExecuter.h"

int GPIOExecuter::GPIODirection(int pin, int dir) {
    char path[35];
    snprintf(path, 35, "/sys/class/gpio/gpio%d/direction", pin);
    int fileDirectory = open(path, O_WRONLY);
    if (fileDirectory == FAIL) {
        //std::cout << "Failed to open GPIO direction for writing!\n" << std::endl;
        return FAIL;
    }
    dir ? write(fileDirectory, "out", 3) : write(fileDirectory, "in", 2);
    close(fileDirectory);
    return 0;
}

int GPIOExecuter::GPIORead(int pin) {
    char path[35];
    char valueFlag[3];
    snprintf(path, 35, "/sys/class/gpio/gpio%d/value", pin);
    int fileDirectory = open(path, O_RDONLY);
    if (fileDirectory == FAIL) {
        //std::cout << "Failed to open gpio value for reading!" << std::endl;
        return FAIL;
    }
    if (read(fileDirectory, valueFlag, 3) == FAIL) {
        //fprintf(stderr, "Failed to read value!\n");
        return FAIL;
    }
    close(fileDirectory);
    return atoi(valueFlag);
}

int GPIOExecuter::GPIOWrite(int pin, int value) {
    static const char s_values_str[] = "01";
    char path[35];
    snprintf(path, 35, "/sys/class/gpio/gpio%d/value", pin);
    int fileDirectory = open(path, O_WRONLY);
    if (fileDirectory == FAIL) {
        //std::cout << "Failed to open gpio value for writing!" << std::endl;
        return FAIL;
    }
    if (1 != write(fileDirectory, &s_values_str[LOW == value ? 0 : 1], 1)) {
        //std::cout << "Failed to write value!" << std::endl;
        return FAIL;
    }
    close(fileDirectory);
    return 0;
}

int GPIOExecuter::GPIOExport(int pin) {
    char buffer[5];
    int fileDirectory = open("/sys/class/gpio/export", O_WRONLY);
    if (fileDirectory == FAIL) {
        //std::cout << "Failed to open \"EXPORT\" for writing!" << std::endl;
        return FAIL;
    } else {
        //std::cout << "\"EXPORT\" opened successfully!" << std::endl;
    }
    ssize_t bytes_written = snprintf(buffer, 5, "%d", pin);
    write(fileDirectory, buffer, bytes_written); // write to a file descriptor
    close(fileDirectory);
    return 0;

}

int GPIOExecuter::GPIOUnexport(int pin) {
    char buffer[3];
    ssize_t bytes_written;
    int fileDirectory = open("/sys/class/gpio/unexport", O_WRONLY);
    if (fileDirectory == FAIL) {
        //std::cout << "Failed to open \"UNEXPORT\" for writing!" << std::endl;
        return FAIL;
    } else {
        //std::cout << "\"UNEXPORT\" opened successfully!" << std::endl;
    }
    bytes_written = snprintf(buffer, 3, "%d", pin);
    write(fileDirectory, buffer, bytes_written);
    close(fileDirectory);
    return 0;
}

