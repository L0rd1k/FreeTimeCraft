/* 
 * File:   TempDetector.h
 * Author: Ilya Petrikov
 * Created on January 29, 2020, 5:04 PM
 */

#ifndef TEMPERATURECONTROLLER_H
#define TEMPERATURECONTROLLER_H

//#define DEV_ADDRESS 0x4e
#define DEV_REGISTERS_NUM 6

class TemperatureController {
public:
    TemperatureController() = default;
    virtual ~TemperatureController() = default;

    void openI2CBus(const char *devName);
    bool getCurrentTemperature(int dev_address, float *temperature);

private:
    int file_i2c = 0;
};

#endif /* TEMPDETECTOR_H */

