import cv2 as cv
import numpy as np
import math

# src_img = cv.imread('inputs_images/complete.jpg')
# cv.imshow('Original Image',src_img)

# dst_img = cv.Canny(src_img, 50, 200, None, 3)

# lines = cv.HoughLines(dst_img, 1, np.pi / 180, 150, None, 0, 0)

# for i in range(0, len(lines)):
#             rho_l = lines[i][0][0]
#             theta_l = lines[i][0][1]
#             a_l = math.cos(theta_l)
#             b_l = math.sin(theta_l)
#             x0_l = a_l * rho_l
#             y0_l = b_l * rho_l
#             pt1_l = (int(x0_l + 1000*(-b_l)), int(y0_l + 1000*(a_l)))
#             pt2_l = (int(x0_l - 1000*(-b_l)), int(y0_l - 1000*(a_l)))
#             cv.line(src_img, pt1_l, pt2_l, (0,0,255), 3, cv.LINE_AA)

# cv.imshow("Image with lines", src_img)
# cv.waitKey(0)




# src_img = cv.imread('inputs_images/two_picture.PNG')
# cv.imshow('Original Image',src_img)

# # Convert the image to grayscale
# gray_img = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)

# # Apply Gaussian blur to reduce noise
# blur_img = cv.GaussianBlur(gray_img, (5,5), 0)

# # Apply thresholding to create a binary image with large white lines
# _, thresh_img = cv.threshold(blur_img, 250, 255, cv.THRESH_BINARY)
# cv.imshow('thresh_img', thresh_img)
# # Detect edges using Canny edge detection with lower and upper thresholds
# edges = cv.Canny(thresh_img, 50, 100)

# # Apply Hough transform to detect lines in the edges image
# lines = cv.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)

# # Draw detected lines on the original image
# for line in lines:
#     x1, y1, x2, y2 = line[0]
#     cv.line(src_img, (x1, y1), (x2, y2), (0, 0, 255), 3)

# cv.imshow('Detected Lines', src_img)
# cv.waitKey(0)

from PIL import Image
import imageio
from skimage.feature import canny
from skimage.morphology import dilation
from scipy import ndimage as ndi
from skimage.measure import label
from skimage.color import label2rgb




src_img = cv.imread('inputs_images/asterix.png')

gray_img = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)
edges = canny(gray_img)
thick_edges = dilation(dilation(edges))
segmentation = ndi.binary_fill_holes(thick_edges)


labels = label(segmentation)

Image.fromarray(np.uint8(label2rgb(labels, bg_label=0) * 255)).show()

print(segmentation)


# Image.fromarray(edges).show()
# Image.fromarray(thick_edges).show()
# Image.fromarray(segmentation).show()
