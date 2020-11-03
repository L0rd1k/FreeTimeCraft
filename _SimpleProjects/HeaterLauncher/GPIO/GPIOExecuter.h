/* 
 * File:   GPIOExecuter.h
 * Author: Ilya Petrikov
 *
 * Created on January 30, 2020, 12:55 PM
 */

#ifndef GPIOEXECUTER_H
#define GPIOEXECUTER_H

#define IN 0
#define OUT 1

#define LOW 0
#define HIGH 1

#define PIN  24
#define POUT 4 

#define FAIL -1

class GPIOExecuter {
public:
    GPIOExecuter() = default;
    virtual ~GPIOExecuter() = default;
public:
    static int GPIOExport(int pin);
    static int GPIOUnexport(int pin);
    static int GPIODirection(int pin, int dir); 
    static int GPIORead(int pin);
    static int GPIOWrite(int pin, int value);
};

#endif /* GPIOEXECUTER_H */

