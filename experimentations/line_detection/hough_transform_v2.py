import cv2
import numpy as np

# Read the image
img = cv2.imread('inputs_images/batman.png')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow("gray", gray)

# Apply binary thresholding
thresh = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
# cv2.imshow("thresh", thresh)

# Apply morphological operations
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))

closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
# cv2.imshow("closed", closed)

invert = cv2.bitwise_not(closed)
# cv2.imshow("invert", invert)

# segmentation = ndi.binary_fill_holes(thick_edges)

# Detect horizontal and vertical lines using Hough Transform
lines = cv2.HoughLinesP(invert, 1, np.pi/180, 100, minLineLength=200, maxLineGap=5)


# TODO reduce number of line

# Draw the detected lines on the original image
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Display the result
cv2.imshow('Detected Lines', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
