import cv2

# Load the image
img = cv2.imread("inputs_images/batman.png")

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply thresholding to create a binary image
_, thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)

# Create a horizontal kernel
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))

# Create a vertical kernel
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))

# Apply morphological operations to detect horizontal and vertical lines
horizontal_lines = cv2.morphologyEx(
    thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2
)
vertical_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

# Display the detected lines
cv2.imshow("Horizontal Lines", horizontal_lines)
cv2.imshow("Vertical Lines", vertical_lines)
cv2.waitKey(0)
