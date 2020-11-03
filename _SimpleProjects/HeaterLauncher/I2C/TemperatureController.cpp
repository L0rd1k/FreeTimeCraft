/* 
 * File:   TempDetector.cpp
 * Author: Ilya Petrikov
 * Created on January 29, 2020, 5:04 PM
 */

#include <string>
#include <iostream>


#include <fcntl.h>
#include <unistd.h> 
#include <io.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <stdlib.h>

#include "TemperatureController.h"

void TemperatureController::openI2CBus(const char *devName) {
    file_i2c = open(devName, O_RDWR);
    if (file_i2c < 0) {
        perror(devName);
    } else {
        std::cout << "Bus " + std::string(devName) + " was found" << std::endl;
    }
}

bool TemperatureController::getCurrentTemperature(int dev_address, float *temperature) {
    if (ioctl(file_i2c, I2C_SLAVE, dev_address) < 0) {
        perror("");
        return false;
    } 
    
    constexpr int byteLength = 2;
    char buffer[10] = {0};
    const int res = read(file_i2c, buffer, byteLength);
    if (res != byteLength) {
        perror("");
        std::cout << "Failed to read from the i2c bus with address " + std::to_string(dev_address) + " ! " << res << std::endl;
        return false;
    }

    float data = float(((buffer[0] & 0xFF) * 256) + (buffer[1] & 0xC0)) / 64;
    if (data > 511) {
        data -= 1024;
    }
    *temperature = data * 0.25;
    return true;
}
