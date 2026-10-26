
import cv2
import numpy as np

# Step 1: Load the road image
image = cv2.imread("images/road1.jpg")

if image is None:
    raise FileNotFoundError("Could not load images/road1.jpg")

print("Image loaded successfully!")

# Step 2: Convert the image from BGR to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Step 3: Define colour limits for white areas
lower_white = np.array([0, 0, 180])
upper_white = np.array([180, 60, 255])

# Step 4: Create a mask to identify white areas
mask = cv2.inRange(hsv, lower_white, upper_white)

cv2.imwrite("outputs/road1_hsv_mask.jpg", mask)

print("HSV colour filtering completed!")
print("Saved result to outputs/road1_hsv_mask.jpg")

# Step 5: Apply Gaussian blur to reduce small irregularities
blurred = cv2.GaussianBlur(mask, (5, 5), 0)

cv2.imwrite("outputs/road1_blurred.jpg", blurred)

print("Gaussian blur completed!")
print("Saved result to outputs/road1_blurred.jpg")

# Step 6: Detect edges using Canny
edges = cv2.Canny(blurred, 50, 150)

# Step 7: Define the region of interest (ROI)
height, width = edges.shape

roi_vertices = np.array([[
    (0, height),
    (width, height),
    (int(width * 0.55), int(height * 0.45)),
    (int(width * 0.45), int(height * 0.45))
]], dtype=np.int32)

# Step 8: Create a black mask and fill the ROI with white
roi_mask = np.zeros_like(edges)

cv2.fillPoly(roi_mask, roi_vertices, 255)

# Step 9: Keep edges only inside the ROI
roi_edges = cv2.bitwise_and(edges, roi_mask)

# Step 10: Save the ROI result
cv2.imwrite("outputs/road1_roi.jpg", roi_edges)

print("ROI masking completed!")
print("Saved result to outputs/road1_roi.jpg")

# Step 11: Detect line segments using Hough Line Transform
lines = cv2.HoughLinesP(
    roi_edges,
    rho=1,
    theta=np.pi / 180,
    threshold=50,
    minLineLength=50,
    maxLineGap=100
)

# Step 12: Draw the detected lines on the original image
line_image = image.copy()

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = np.array(line).reshape(-1)[:4]

        cv2.line(
            line_image,
            (int(x1), int(y1)),
            (int(x2), int(y2)),
            (0, 0, 255),
            5
        )

# Step 13: Save the final result
cv2.imwrite("outputs/road1_lane_lines.jpg", line_image)

print("Lane line detection completed!")
print("Saved result to outputs/road1_lane_lines.jpg")

# Step 7: Save the edge-detected image
cv2.imwrite("outputs/road1_edges.jpg", edges)

print("Canny edge detection completed!")
print("Saved result to outputs/road1_edges.jpg")
