## 1) Canny Edge Detector
  | Step | Description | Image |
|----------------|:---------:|----------------:|
| 1 | Grayscaling. | ![Alt-текст](https://github.com/L0rd1k/WolrdAroundPython/blob/master/Images/Canny/Original.png "Original") |
| 2 | Grayscaling. | ![Alt-текст](https://github.com/L0rd1k/WolrdAroundPython/blob/master/Images/Temp_test/Canny_Grayscale.png "Grayscaled") |
| 3 | Gaussian Smoothing (Noise reduction). ![Alt-текст](https://github.com/L0rd1k/WolrdAroundPython/blob/master/Images/Canny/Gaussian%20filter%20kernel.png "Gaussian Smoothing")|  ![Alt-текст](https://github.com/L0rd1k/WolrdAroundPython/blob/master/Images/Temp_test/Canny_Smoothing.png "Smoothed") |
| 4 | Gradient calculation.Calculate Edge intensity, horizontal for Gx and vertical for Gy using Sobel kernels Kx Ky. ![Alt-текст](https://github.com/L0rd1k/WolrdAroundPython/blob/master/Images/Canny/Sobel%20Kernel.png "Sobel Kernel") |  ![Alt-текст](https://github.com/L0rd1k/WolrdAroundPython/blob/master/Images/Canny/Gradient%20Sobel.jpg "Smoothed") |
| 5 | Calculate Magnitude of the gradient. ![Alt-текст](https://github.com/L0rd1k/WolrdAroundPython/blob/master/Images/Canny/Magnitude.png "Magnitude")  | ![Alt-текст](https://github.com/L0rd1k/WolrdAroundPython/blob/master/Images/Canny/Gradient%20Magnitude.jpg "Smoothed")   |
| 6 | Calculate Slope (edge orientation) of the gradient. | ![Alt-текст](https://github.com/L0rd1k/WolrdAroundPython/blob/master/Images/Canny/Gradient%20Magnitude.jpg "Smoothed")  |
| 7 | Non-Maximum Suppression: makes edges a bit thinner. The algorithm goes through all the points on the gradient intensity matrix and finds the pixels with the maximum value in the edge directions.  ![Alt-текст](https://github.com/L0rd1k/WolrdAroundPython/blob/master/Images/Canny/non%20maximum%20suppression.png "Smoothed") | ![Alt-текст](https://github.com/L0rd1k/WolrdAroundPython/blob/master/Images/Canny/suppressed.jpg "Smoothed")  |
| 8 | Double threshold: finds 3 kinds of pixels: string, weak and non-relevant.|  ![Alt-текст](https://github.com/L0rd1k/WolrdAroundPython/blob/master/Images/Canny/temp.jpg "Smoothed")|
| 9 | Edge Tracking by Hysteresis: transforming weak pixels into strong ones, if and only if at least one of the pixels around the one being processed is a strong one. ![Alt-текст](https://github.com/L0rd1k/WolrdAroundPython/blob/master/Images/Canny/Hysteresis.png "Smoothed") | ![Alt-текст](https://github.com/L0rd1k/WolrdAroundPython/blob/master/Images/Canny/canny_result.jpg "Smoothed")  |
____
2) Gaussian Smoothing Filter
____
3) Sobel Edge Detector
____
4) HOG(Histogram of oriented gradients) descriptor
____
5) Laplacian edge detector
____
7) HOG + SVM template matching
____
