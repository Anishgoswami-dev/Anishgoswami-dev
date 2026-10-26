import cv2
import numpy as np

img = cv2.imread("input/photo.png")
h, w = img.shape[:2]

# Define polygon points tracing Anish's actual silhouette
pts = np.array([
    # Hair top
    [185, 48], [200, 42], [220, 38], [240, 42], [260, 50], [275, 65], [280, 85], [280, 115],
    # Right ear / jaw / neck
    [268, 125], [265, 140], [262, 160], [258, 180], [252, 215],
    # Right shoulder & torso
    [265, 222], [290, 230], [320, 245], [350, 265], [365, 290], [370, 340], [370, 395],
    # Bottom
    [60, 395],
    # Left torso & shoulder
    [65, 340], [75, 290], [95, 265], [130, 245], [160, 230], [192, 218],
    # Left neck & chin & glasses & hair
    [198, 200], [195, 180], [188, 165], [182, 148], [175, 125],
    [170, 105], [170, 80], [178, 60], [185, 48]
], np.int32)

mask = np.zeros((h, w), dtype=np.uint8)
cv2.fillPoly(mask, [pts], 255)

# Soften mask boundary slightly (anti-aliased edge)
mask_blurred = cv2.GaussianBlur(mask, (5, 5), 0)

b, g, r = cv2.split(img)
bgra = cv2.merge([b, g, r, mask_blurred])
cv2.imwrite("scripts/ascii/_work/cutout_poly.png", bgra)
print("Saved scripts/ascii/_work/cutout_poly.png")
