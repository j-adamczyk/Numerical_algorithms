# Laboratory 9 - FFT applications

## Task 1 - using FFT for image recognition
Fast Fourier Transform (FFT) can be used for pattern recognition. It uses convolution theorem to, in a way, create very fast "sliding window" for 
detecting given pattern in another image with given threshold. FFT can also be used to calculate correlation "by hand", 
but convolution does it automatically, in a way. It's tested on 2 images: simple text (finding letter "e") and image
of a school of fish (finding individual fishes). The second one is more interesting, since for better results it requires using 
only Red channel of RGB image (since it's the differentiating factor - blue and green are ubiquitous in sea photos).

## Task 2 - Optical Character Recognition (OCR)
Using aformentioned convolution theorem FFT can also be used for OCR of scanned texts. The program takes a scan of a document, 
rotates it with OpenCV to make text lines horizontal, filters noise with FFT high-pass filter, 
scans for individual letters using FFT convolution and returns text. The efficiency is not very high because of the simplicity, but 
for texts of good quality it works quite fine.