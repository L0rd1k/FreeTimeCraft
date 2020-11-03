/* 
 * File:   TemperatureCalculator.h
 * Author: Ilya Petrikov
 */

#ifndef TEMPERATURECALCULATOR_H
#define TEMPERATURECALCULATOR_H

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <iostream>
#include <string>
#include <algorithm> 
#include <cmath>

#define OBJECT_RADIUS 15
#define MOUSE_RADIUS 25

struct HeaterInfo {
    HeaterInfo() = default;
    HeaterInfo(cv::Point pixPos, double temp) :
    _pixelPosition(pixPos),
    _temperature(temp) {
    }
    cv::Point _pixelPosition;
    double _temperature = 0.0;
};

class TemperatureCalculator {
public:
    TemperatureCalculator(std::string path);
    void LoadInfraredVideo();
    void GetPixelIntensity(cv::Mat frame);
    void getMaxMinTemperatureTreshold(cv::Mat frame);
    
    double CalculateMedianValue(std::vector<double> values);
    double CalculateAverageValue(std::vector<double> values);
    
    double CelsiusToKelvin(double degree);
    double KelvinToCelsius(double degree);
    int RetrieveMaxPixelsInArea(cv::Point centerPixel);
    double RetrieveMaxTemperatureInArea(cv::Point centerPixel);
    
    void OnMouseHoverClass(int event, int x, int y);
    void calcCurrentDegree();
    static void OnMouseHover(int event, int x, int y, int flags, void* userdata);
    
    void TresholdRetriever(cv::Mat frame, int thresholdMax, int thresholdMin);
    
    virtual ~TemperatureCalculator();
private:
    template <class T>
    void GetPixelsBrightnessInRadius(cv::Point currentPos, std::vector<T> &vecValues, int radius) {
        for (int i = currentPos.x - radius; i < currentPos.x + radius; i++) {
            for (int j = currentPos.y - radius; j < currentPos.y + radius; j++) {
                auto currentTemp = _grayFrame.at<uchar>(cv::Point(i, j));
                vecValues.push_back(currentTemp);
            }
        }
    };
    template <class T>
    void GetPixelsTemperatureInRadius(cv::Point currentPos, std::vector<T> &vecValues, int radius) {
        for (int i = currentPos.x - radius; i < currentPos.x + radius; i++) {
            for (int j = currentPos.y - radius; j < currentPos.y + radius; j++) {
                auto currentTemp = matTemperatures.at<double>(cv::Point(i, j));
                vecValues.push_back(currentTemp);
            }
        }
    };
private:
    std::string _videoPath;
    cv::Mat _currentFrame, _grayFrame;
    cv::VideoCapture capture;
    HeaterInfo heat[2];
    int maxBrightness = 0;
    cv::Mat matTemperatures;
    cv::Point currentPos, centerPixel, lastPosition;
    double k, b;
};

#endif /* TEMPERATURECALCULATOR_H */

