from time import sleep
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
from skimage.feature import canny
from skimage.morphology import dilation
from scipy import ndimage as ndi
from skimage.measure import label, regionprops
from skimage.color import label2rgb




src_img = cv.imread('inputs_images/batman.png')

Image.fromarray(src_img).show()

gray_img = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)
edges = canny(gray_img)

thick_edges = edges
# Image.fromarray(thick_edges).show()

segmentation = ndi.binary_fill_holes(thick_edges)
labels = label(segmentation)

# Image.fromarray(np.uint8(label2rgb(labels, bg_label=0) * 255)).show()



def do_bboxes_overlap(a, b):
    return (
        a[0] < b[2] and
        a[2] > b[0] and
        a[1] < b[3] and
        a[3] > b[1]
    )

def merge_bboxes(a, b):
    return (
        min(a[0], b[0]),
        min(a[1], b[1]),
        max(a[2], b[2]),
        max(a[3], b[3])
    )

regions = regionprops(labels)
panels = []

for region in regions:

    for i, panel in enumerate(panels):
        if do_bboxes_overlap(region.bbox, panel):
            panels[i] = merge_bboxes(panel, region.bbox)
            break
    else:
        panels.append(region.bbox)

for i, bbox in reversed(list(enumerate(panels))):
    area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
    if area < 0.01 * src_img.shape[0] * src_img.shape[1]:
        del panels[i]


panel_img = np.zeros_like(labels)

for i, bbox in enumerate(panels, start=1):
    # panel_img[bbox[0]:bbox[2], bbox[1]:bbox[3]] = i
    # if i == 2:
    #     break
    panel = src_img[bbox[0]:bbox[2], bbox[1]:bbox[3]]
    # Image.fromarray(panel).show()
    cv.imwrite(f"outputs/batman_panel_{i}.png", panel)
    # Image.fromarray(np.uint8(label2rgb(panel, bg_label=0) * 255)).show()

# Image.fromarray(np.uint8(label2rgb(panel_img, bg_label=0) * 255)).show()

cv.waitKey(0)