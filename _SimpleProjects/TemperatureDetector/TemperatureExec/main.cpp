#include <cstdlib>
#include <iostream>
#include "TemperatureCalculator.h"

int main(int, char**) {
    TemperatureCalculator temp_c("rtsp://192.168.1.111/onvif/media/PRF08.wxp");
    // TemperatureCalculator temp_c("./test_avg2.avi");
    temp_c.LoadInfraredVideo();
    return 0;
}