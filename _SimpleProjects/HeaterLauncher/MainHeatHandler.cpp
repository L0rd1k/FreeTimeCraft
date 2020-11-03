/* 
 * File:   MainHeatHandler.cpp
 * Author: Ilya Petrikov
 * 
 * Created on February 3, 2020, 10:59 AM
 */

#include <iostream>
#include <thread>

#include "MainHeatHandler.h"

MainHeatHandler::MainHeatHandler() {
    _glasses[OES_FRONT_GLASS] = HeaterInfo(0x4E, 480);
    _glasses[OES_BACK_GLASS] = HeaterInfo(0x4C, 388);
    _glasses[OES_DOWN_GLASS] = HeaterInfo(0x4F, 486);

    _tempControl.openI2CBus(devName);

    for (const auto &glass : _glasses) {
        _gpioExec.GPIOExport(glass.second.heaterGPIONumber);
        _gpioExec.GPIODirection(glass.second.heaterGPIONumber, OUT);
        _gpioExec.GPIOWrite(glass.second.heaterGPIONumber, 0);
    }
}

void MainHeatHandler::heatLauncher() {
    for(;;) {
        getTemperatures();
        getHeaterStates();
        checkOffConditions();
        checkOnConditions();
        print();
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
}

void MainHeatHandler::getTemperatures() {
    for (auto &glass : _glasses) {
        auto &glassState = glass.second;
        glassState.temperatureValid = 
            _tempControl.getCurrentTemperature(glassState.heaterAddress, &glassState.temperature);
    }
}

void MainHeatHandler::getHeaterStates() {
    for (auto &glass : _glasses) {
        const auto previousState = glass.second;
        glass.second.heaterState =_gpioExec.GPIORead(glass.second.heaterGPIONumber);
        glass.second.heaterStateValid = glass.second.heaterState >= 0;

        if(previousState.heaterStateValid && glass.second.heaterStateValid) {
            if(previousState.heaterState == 0 && glass.second.heaterState == 1) {
                glass.second.heaterStart = Clock::now();
            } else if(previousState.heaterState == 1 && glass.second.heaterState == 0) {
                glass.second.heaterEnd = Clock::now();
            }
        }
    }
}

void MainHeatHandler::checkOffConditions() {
    for (const auto &glass : _glasses) {
        const auto glassState = glass.second;
        const auto diff = std::chrono::duration_cast<std::chrono::seconds>(Clock::now() - glassState.heaterStart);
        if(!glassState.temperatureValid || 
           !glassState.heaterStateValid ||
           glassState.temperature > maxValueTemp ||
           (glassState.heaterState && diff.count() >= maxTimeHeat)) {
            _gpioExec.GPIODirection(glassState.heaterGPIONumber, OUT);
            _gpioExec.GPIOWrite(glassState.heaterGPIONumber, 0);    
        }
    }
}

void MainHeatHandler::checkOnConditions() {
    OESON_GLASSES glassToHeat = NONE;
    for (const auto &glass : _glasses) {
        const auto glassState = glass.second;
        if(!glassState.heaterStateValid || glassState.heaterState) {
            return;
        }

        const auto diff = std::chrono::duration_cast<std::chrono::seconds>(Clock::now() - glassState.heaterEnd);
        if(glassState.heaterStateValid && !glassState.heaterState && 
           glassState.temperature < minValueTemp && diff.count() >= maxTimePause) {
            glassToHeat = glass.first;
        }
    }

    if(_glasses.count(glassToHeat)) {
        _gpioExec.GPIODirection(_glasses.at(glassToHeat).heaterGPIONumber, OUT);
        _gpioExec.GPIOWrite(_glasses.at(glassToHeat).heaterGPIONumber, 1);
    }
}

void MainHeatHandler::print() {
    std::cout << " ========================================== " << std::endl;
    for (const auto &glass : _glasses) {
        std::cout << "Glass " << glass.first << std::endl;
        const std::string temperature = glass.second.temperatureValid ? 
                std::to_string(glass.second.temperature) : "UNKNOWN";
        std::cout << "Temperature: " << temperature << std::endl;
        const std::string heater = glass.second.heaterStateValid ? 
                std::to_string(glass.second.heaterState) : "UNKNOWN";
        std::cout << "Heater: " << heater << std::endl;
    }
}
