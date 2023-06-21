import cv2
import numpy as np

# Load the image
img = cv2.imread("inputs_images/batman.png")

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply canny edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Detect horizontal lines using Hough Transform
minLineLength = 100
maxLineGap = 10
horizontal_lines = cv2.HoughLinesP(
    edges, 1, np.pi / 180, 100, minLineLength, maxLineGap
)

# Draw horizontal lines on the original image
for line in horizontal_lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Rotate the image by 90 degrees
rotated_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

# Apply the same process to detect vertical lines
gray_rotated = cv2.cvtColor(rotated_img, cv2.COLOR_BGR2GRAY)
edges_rotated = cv2.Canny(gray_rotated, 50, 150, apertureSize=3)
vertical_lines = cv2.HoughLinesP(
    edges_rotated, 1, np.pi / 180, 100, minLineLength, maxLineGap
)
for line in vertical_lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(rotated_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Rotate the image back by 90 degrees
final_img = cv2.rotate(rotated_img, cv2.ROTATE_90_COUNTERCLOCKWISE)

# Display the final image
cv2.imshow("Detected Lines", final_img)
cv2.waitKey(0)
