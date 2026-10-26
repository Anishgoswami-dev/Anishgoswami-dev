import cv2
import numpy as np

img = cv2.imread("input/photo.png")
h, w = img.shape[:2]

# Anish Goswami's exact profile silhouette
# Looking slightly 3/4 to the left, wearing sunglasses and yellow kurta
head_contour = [
    # Top hair arc
    [190, 48], [210, 40], [230, 38], [250, 42], [268, 52], [278, 68], [280, 90], [280, 115],
    # Right ear & jawline
    [268, 125], [264, 142], [260, 165], [256, 185], [250, 215],
    # Right shoulder slope
    [265, 222], [290, 230], [320, 245], [345, 265], [360, 290], [365, 325], [360, 360],
    # Bottom curved bust border (tapering to a point/arc like reference bust)
    [330, 375], [290, 385], [240, 390], [200, 390], [150, 385], [110, 375], [80, 360],
    # Left shoulder slope
    [75, 325], [80, 290], [95, 265], [125, 245], [155, 230], [190, 218],
    # Left neck, chin, mustache, sunglasses, forehead
    [195, 205], [192, 185], [186, 168], [178, 150], [172, 130],
    [168, 115], [170, 95], [175, 75], [182, 60]
]

pts = np.array(head_contour, np.int32)
mask = np.zeros((h, w), dtype=np.uint8)
cv2.fillPoly(mask, [pts], 255)

# Smooth edges with slight blur for soft anti-aliased transition
mask_smooth = cv2.GaussianBlur(mask, (5, 5), 0)

b, g, r = cv2.split(img)
bgra = cv2.merge([b, g, r, mask_smooth])

cv2.imwrite("scripts/ascii/_work/prepped/f00.png", bgra)
print("Saved clean f00.png with exact Anish Goswami silhouette!")
