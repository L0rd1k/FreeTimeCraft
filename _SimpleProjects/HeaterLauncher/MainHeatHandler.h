/* 
 * File:   MainHeatHandler.h
 * Author: Ilya Petrikov
 *
 * Created on February 3, 2020, 10:59 AM
 */

#ifndef MAINHEATHANDLER_H
#define MAINHEATHANDLER_H

#include <map>
#include <vector>
#include <chrono>

#include "I2C/TemperatureController.h"
#include "GPIO/GPIOExecuter.h"

typedef std::chrono::high_resolution_clock Clock;

enum OESON_GLASSES {
    NONE = -1,
    OES_FRONT_GLASS = 0,
    OES_BACK_GLASS = 1,
    OES_DOWN_GLASS = 2
};

struct HeaterInfo {
    unsigned long heaterAddress = 0;
    int heaterGPIONumber = 0;

    float temperature = 0;
    bool temperatureValid = false;

    bool heaterState = false;
    bool heaterStateValid = false;

    std::chrono::time_point<Clock> heaterStart = Clock::now();
    std::chrono::time_point<Clock> heaterEnd = Clock::now();
    
    HeaterInfo() = default;

    HeaterInfo(unsigned long heaterAddress, int heaterGPIONumber) :
    heaterAddress(heaterAddress),
    heaterGPIONumber(heaterGPIONumber) {}
};

class MainHeatHandler {
public:
    MainHeatHandler();
    virtual ~MainHeatHandler() = default;

    void heatLauncher();

private:
    GPIOExecuter _gpioExec;
    TemperatureController _tempControl;
    std::map<OESON_GLASSES, HeaterInfo> _glasses;

    const char *devName = "/dev/i2c-0";
    const float minValueTemp = 6.0f;
    const float maxValueTemp = 10.0f;
    const float maxTimeHeat = 30.0f;
    const float maxTimePause = 10.0f;
    
    void getTemperatures();
    void getHeaterStates();
    void checkOffConditions();
    void checkOnConditions();
    void print();
};

#endif /* MAINHEATHANDLER_H */
