import cv2
import numpy as np

# Read the image
img = cv2.imread("inputs_images/batman.png")

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Apply probabilistic Hough Transform to detect lines
lines = cv2.HoughLinesP(
    edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=5
)

# Fit lines to the detected edges using RANSAC
for line in lines:
    x1, y1, x2, y2 = line[0]
    points = np.array([[x1, y1], [x2, y2]])
    v = cv2.fitLine(points, cv2.DIST_L2, 0, 0.01, 0.01)
    k = v[1] / v[0]
    b = y1 - k * x1
    cv2.line(
        img, (0, int(b)), (img.shape[1], int(k * img.shape[1] + b)), (0, 0, 255), 2
    )

# Display the result
cv2.imshow("Detected Lines", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
