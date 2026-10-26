
import cv2
import numpy as np

image = cv2.imread("images/road1.jpg")

if image is None:
    raise FileNotFoundError("Could not load images/road1.jpg")

print("Image loaded successfully!")

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_white = np.array([0, 0, 180])
upper_white = np.array([180, 60, 255])

mask = cv2.inRange(hsv, lower_white, upper_white)

cv2.imwrite("outputs/road1_hsv_mask.jpg", mask)

print("HSV colour filtering completed!")
print("Saved result to outputs/road1_hsv_mask.jpg")

blurred = cv2.GaussianBlur(mask, (5, 5), 0)

cv2.imwrite("outputs/road1_blurred.jpg", blurred)

print("Gaussian blur completed!")
print("Saved result to outputs/road1_blurred.jpg")

edges = cv2.Canny(blurred, 50, 150)

height, width = edges.shape

roi_vertices = np.array([[
    (0, height),
    (width, height),
    (int(width * 0.55), int(height * 0.45)),
    (int(width * 0.45), int(height * 0.45))
]], dtype=np.int32)

roi_mask = np.zeros_like(edges)

cv2.fillPoly(roi_mask, roi_vertices, 255)

roi_edges = cv2.bitwise_and(edges, roi_mask)

cv2.imwrite("outputs/road1_roi.jpg", roi_edges)

print("ROI masking completed!")
print("Saved result to outputs/road1_roi.jpg")

lines = cv2.HoughLinesP(
    roi_edges,
    rho=1,
    theta=np.pi / 180,
    threshold=50,
    minLineLength=50,
    maxLineGap=100
)

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

cv2.imwrite("outputs/road1_lane_lines.jpg", line_image)

print("Lane line detection completed!")
print("Saved result to outputs/road1_lane_lines.jpg")

cv2.imwrite("outputs/road1_edges.jpg", edges)

print("Canny edge detection completed!")
print("Saved result to outputs/road1_edges.jpg")
