/* 
 * File:   TemperatureCalculator.cpp
 * Author: Ilya Petrikov
*/

#include <opencv2/highgui.hpp>
#include "TemperatureCalculator.h"


TemperatureCalculator::TemperatureCalculator(std::string path) {
    _videoPath = path;
    
    
    //    heat[1] = HeaterInfo(cv::Point(745, 202), 33.0); // test12
    //    heat[0] = HeaterInfo(cv::Point(563, 312), 31.0);
    //    heat[1] = HeaterInfo(cv::Point(720, 314), 30.6); // test13
    //    heat[0] = HeaterInfo(cv::Point(224, 300), 23.7);
    //    heat[1] = HeaterInfo(cv::Point(690, 540), 37.0); // test14
    //    heat[0] = HeaterInfo(cv::Point(127, 297), 24.4);
    //    heat[1] = HeaterInfo(cv::Point(652, 544), 47.0); // test15
    //    heat[0] = HeaterInfo(cv::Point(81, 301), 24.5);

    heat[0] = HeaterInfo(cv::Point(696, 281), 24.9); // test16
    //    heat[1] = HeaterInfo(cv::Point(679, 191), 31.0);
    heat[1] = HeaterInfo(cv::Point(538, 520), 45.7);
    //    heat[1] = HeaterInfo(cv::Point(307, 311), 31.6);
}

void TemperatureCalculator::calcCurrentDegree() {
    std::vector<double> pixelsTemp;
    GetPixelsTemperatureInRadius(currentPos, pixelsTemp, MOUSE_RADIUS);
    auto currentDegree = CalculateMedianValue(pixelsTemp);
    cv::putText(_currentFrame, "Degree: " + std::to_string(currentDegree), cv::Point(10, 25),
            cv::FONT_HERSHEY_DUPLEX, 1.0, CV_RGB(0, 255, 0), 1);
}

int TemperatureCalculator::RetrieveMaxPixelsInArea(cv::Point centerPixel) {
    std::vector<int> pixelValues;
    GetPixelsBrightnessInRadius(centerPixel, pixelValues, OBJECT_RADIUS);
    maxBrightness = *std::max_element(pixelValues.begin(), pixelValues.end());
    std::cout << "Max brightness: " << maxBrightness << std::endl;
    return maxBrightness;
}

double TemperatureCalculator::RetrieveMaxTemperatureInArea(cv::Point centerPixel) {
    std::vector<double> pixelValues;
    GetPixelsTemperatureInRadius(centerPixel, pixelValues, OBJECT_RADIUS);
    for (auto elem : pixelValues) {
        std::cout << elem << std::endl;
    }
    std::cout << "=================" << std::endl;
    double maxTemp = *std::max_element(pixelValues.begin(), pixelValues.end());
    std::cout << "Max temperature: " << maxTemp << std::endl;
    return maxTemp;
}

void TemperatureCalculator::TresholdRetriever(cv::Mat frame, int thresholdMax, int thresholdMin) {
    cv::Mat _cframe = frame.clone();
    cv::threshold(frame, _cframe, thresholdMin + thresholdMax / 2, thresholdMax, cv::THRESH_BINARY);
    cv::imshow("Thresh", _cframe);
}

void TemperatureCalculator::OnMouseHoverClass(int event, int x, int y) {
    cv::Point p(x, y);
    currentPos = p;
    if (event == cv::EVENT_MOUSEMOVE) {
        std::vector<double> pixValue;
        GetPixelsTemperatureInRadius(currentPos, pixValue, MOUSE_RADIUS);
        double maxTemp = *std::max_element(pixValue.begin(), pixValue.end());
        double realTemp = matTemperatures.at<double>(currentPos);
        double medianTemp = CalculateMedianValue(pixValue);
        //        double temperatureAvg = CalculateAverageValue(pixValue);
        std::cout << "Median Temp: " << std::to_string(medianTemp) <<
                "/ Max Temp: " << maxTemp <<
                "/ Real Temp: " << realTemp << std::endl;

    } else if (event == cv::EVENT_LBUTTONDBLCLK) {

        std::vector<double> pixelTempValues;
        std::vector<double> pixelBrightValues;
        GetPixelsTemperatureInRadius(currentPos, pixelTempValues, MOUSE_RADIUS);
        GetPixelsBrightnessInRadius(currentPos, pixelBrightValues, MOUSE_RADIUS);
        double temperature = CalculateMedianValue(pixelTempValues);
        double brightness = CalculateMedianValue(pixelBrightValues);

        double maxTemp = *std::max_element(pixelTempValues.begin(), pixelTempValues.end());
        double maxBrightTemp = *std::max_element(pixelBrightValues.begin(), pixelBrightValues.end());

        cv::rectangle(_currentFrame, cv::Point(currentPos.x - MOUSE_RADIUS, currentPos.y - MOUSE_RADIUS),
                cv::Point(currentPos.x + MOUSE_RADIUS, currentPos.y + MOUSE_RADIUS),
                cv::Scalar(255, 255, 0), 1, cv::LINE_4);

        cv::putText(_currentFrame, "T-mid:" + std::to_string(int(temperature)), cv::Point(currentPos.x - 40, currentPos.y - 15),
                cv::FONT_HERSHEY_DUPLEX, 0.5, CV_RGB(255, 0, 255), 1);
        cv::putText(_currentFrame, "T-max:" + std::to_string(int(maxTemp)), cv::Point(currentPos.x - 40, currentPos.y - 30),
                cv::FONT_HERSHEY_DUPLEX, 0.5, CV_RGB(255, 0, 255), 1);
        cv::putText(_currentFrame, "B-mid:" + std::to_string(int(brightness)), cv::Point(currentPos.x - 40, currentPos.y - 45),
                cv::FONT_HERSHEY_DUPLEX, 0.5, CV_RGB(255, 0, 255), 1);
        cv::putText(_currentFrame, "B-max:" + std::to_string(int(maxBrightTemp)), cv::Point(currentPos.x - 40, currentPos.y - 60),
                cv::FONT_HERSHEY_DUPLEX, 0.5, CV_RGB(255, 0, 255), 1);

        cv::imshow("Frame", _currentFrame);
        std::cout << "Max temperature: " << maxTemp << std::endl;
    }
}

void TemperatureCalculator::OnMouseHover(int event, int x, int y, int flags, void* userdata) {
    if (userdata != nullptr) {
        TemperatureCalculator* settings = reinterpret_cast<TemperatureCalculator*> (userdata);
        settings->OnMouseHoverClass(event, x, y);
    } else {

        std::cout << "NULL" << std::endl;
    }
}

double TemperatureCalculator::CalculateMedianValue(std::vector<double> values) {
    if (values.size() != 0) {
        std::sort(values.begin(), values.end());
        if (values.size() % 2 == 0)
            return (values[values.size() / 2 - 1] + values[values.size() / 2]) / 2;
        else
            return values[values.size() / 2];
    }
}

double TemperatureCalculator::CalculateAverageValue(std::vector<double> values) {
    if (values.size() != 0) {
        double sum;
        for (auto elem : values) {
            sum += elem;
        }
        return (sum / values.size());
    }
}

double TemperatureCalculator::CelsiusToKelvin(double degree) {
    return degree + 273.15;
}

double TemperatureCalculator::KelvinToCelsius(double degree) {
    return degree - 273.15;
}

void TemperatureCalculator::GetPixelIntensity(cv::Mat frame) {
    double temp1 = heat[0]._temperature;
    double temp2 = heat[1]._temperature;


    //    int pxl1 = frame.at<uchar>(heat[0]._pixelPosition);
    //    int pxl2 = frame.at<uchar>(heat[1]._pixelPosition);
    double pxl1 = RetrieveMaxPixelsInArea(heat[0]._pixelPosition); //    double p1 = frame.at<uchar>(heat[0]._pixelPosition);
    double pxl2 = RetrieveMaxPixelsInArea(heat[1]._pixelPosition); //    double p2 = frame.at<uchar>(heat[1]._pixelPosition);

    for (auto i = 0; i < 2; i++) {
        cv::rectangle(_currentFrame, cv::Point(heat[i]._pixelPosition.x - OBJECT_RADIUS, heat[i]._pixelPosition.y - OBJECT_RADIUS),
                cv::Point(heat[i]._pixelPosition.x + OBJECT_RADIUS, heat[i]._pixelPosition.y + OBJECT_RADIUS),
                cv::Scalar(255, 255, 0), 1, cv::LINE_4);
    }

    k = (temp1 - temp2) / (pxl1 - pxl2);
    b = (temp1 * pxl2 - temp2 * pxl1) / (pxl2 - pxl1);

    for (auto i = 0; i < frame.rows; i++) {
        for (auto j = 0; j < frame.cols; j++) {
            double pixelBrightness = frame.at<uchar>(i, j);
            double temperature = k * pixelBrightness + b;
            matTemperatures.at<double>(i, j) = temperature;
        }
    }

    double pixelsBrightness[2] = {pxl1, pxl2};
    for (int i = 0; i < 2; i++) {
        double maxPixel = RetrieveMaxPixelsInArea(heat[i]._pixelPosition);
        double maxTemperature = RetrieveMaxTemperatureInArea(heat[i]._pixelPosition);

        std::vector<double> brightVec;
        GetPixelsBrightnessInRadius(heat[i]._pixelPosition, brightVec, OBJECT_RADIUS);
        double medianBright = CalculateMedianValue(brightVec);

        std::vector<double> tempVec;
        GetPixelsTemperatureInRadius(heat[i]._pixelPosition, tempVec, OBJECT_RADIUS);
        double medianTemp = CalculateMedianValue(tempVec);

        cv::putText(_currentFrame,
                "T: " + std::to_string(int(maxTemperature)), cv::Point(heat[i]._pixelPosition.x - 40, heat[i]._pixelPosition.y),
                cv::FONT_HERSHEY_DUPLEX, 0.4, CV_RGB(255, 0, 0), 1);
        cv::putText(_currentFrame,
                "Tc: " + std::to_string(int(matTemperatures.at<double>(heat[i]._pixelPosition))), cv::Point(heat[i]._pixelPosition.x - 40, heat[i]._pixelPosition.y - 15),
                cv::FONT_HERSHEY_DUPLEX, 0.4, CV_RGB(255, 0, 0), 1);
        cv::putText(_currentFrame,
                "B: " + std::to_string(int(maxPixel)), cv::Point(heat[i]._pixelPosition.x - 40, heat[i]._pixelPosition.y - 30),
                cv::FONT_HERSHEY_DUPLEX, 0.4, CV_RGB(255, 0, 0), 1);
        cv::putText(_currentFrame,
                "Bc: " + std::to_string(int(pixelsBrightness[i])), cv::Point(heat[i]._pixelPosition.x - 40, heat[i]._pixelPosition.y - 45),
                cv::FONT_HERSHEY_DUPLEX, 0.4, CV_RGB(255, 0, 0), 1);
        cv::putText(_currentFrame,
                "Bm: " + std::to_string(int(medianBright)), cv::Point(heat[i]._pixelPosition.x - 40, heat[i]._pixelPosition.y - 60),
                cv::FONT_HERSHEY_DUPLEX, 0.4, CV_RGB(255, 0, 0), 1);
        cv::putText(_currentFrame,
                "Tm: " + std::to_string(int(medianTemp)), cv::Point(heat[i]._pixelPosition.x - 40, heat[i]._pixelPosition.y - 75),
                cv::FONT_HERSHEY_DUPLEX, 0.4, CV_RGB(255, 0, 0), 1);
    }
}

void TemperatureCalculator::LoadInfraredVideo() {
    cv::VideoCapture capture;
    capture.open(_videoPath);
    if (!capture.isOpened())
        return;
    capture >> _currentFrame;
    matTemperatures.create(_currentFrame.rows, _currentFrame.cols, CV_64F); // create 2D matrix for temperatures 
    while (true) {
        capture >> _currentFrame;
        cv::cvtColor(_currentFrame, _grayFrame, cv::COLOR_RGB2GRAY);
        GetPixelIntensity(_grayFrame);
        cv::namedWindow("Frame", 1);
        cv::setMouseCallback("Frame", OnMouseHover, this);
        //calcCurrentDegree();
        cv::imshow("Frame", _currentFrame);
        int key = cv::waitKey(0);
        if (key == 27) {
            break;
        } else if (key == ' ') {
            cv::waitKey();
        }
    }
}

TemperatureCalculator::~TemperatureCalculator() {
}

