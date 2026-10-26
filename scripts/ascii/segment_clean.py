import cv2
import numpy as np

img = cv2.imread("input/photo.png")
h, w = img.shape[:2]
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Mask setup
mask = np.zeros((h, w), np.uint8)

# Circular avatar boundary
cy, cx, r = 200, 218, 185
Y, X = np.ogrid[:h, :w]
outside_circle = ((X - cx)**2 + (Y - cy)**2) > (r**2)
mask[outside_circle] = cv2.GC_BGD

# 1. Detect yellow kurta
# In HSV, yellow is roughly H: 18-40, S: 70-255, V: 80-255
kurta_mask = (
    (hsv[:, :, 0] >= 16) & (hsv[:, :, 0] <= 42) &
    (hsv[:, :, 1] >= 60) &
    (hsv[:, :, 2] >= 90) &
    (Y >= 180) & (X >= 60) & (X <= 375)
)

# 2. Detect dark hair & sunglasses & beard
dark_features = (
    (hsv[:, :, 2] <= 70) &
    (Y >= 35) & (Y <= 200) &
    (X >= 155) & (X <= 285)
)

# 3. Detect skin in head & neck
skin_mask = (
    (hsv[:, :, 0] >= 3) & (hsv[:, :, 0] <= 25) &
    (hsv[:, :, 1] >= 30) & (hsv[:, :, 1] <= 180) &
    (hsv[:, :, 2] >= 80) &
    (Y >= 60) & (Y <= 230) &
    (X >= 160) & (X <= 275)
)

# Set definite foreground
mask[kurta_mask] = cv2.GC_FGD
mask[dark_features] = cv2.GC_FGD
mask[skin_mask] = cv2.GC_FGD

# Set probable foreground around head
head_envelope = (Y >= 35) & (Y <= 220) & (X >= 155) & (X <= 285)
mask[head_envelope & (mask == 0)] = cv2.GC_PR_FGD

# Set probable foreground around torso
torso_envelope = (Y >= 210) & (Y <= 390) & (X >= 75) & (X <= 365)
mask[torso_envelope & (mask == 0)] = cv2.GC_PR_FGD

# Set background outside the person's envelope
person_envelope = (
    ((Y >= 35) & (Y <= 220) & (X >= 150) & (X <= 290)) |
    ((Y > 210) & (Y <= 395) & (X >= 65) & (X <= 375))
)
mask[~person_envelope & ~outside_circle] = cv2.GC_BGD

# GrabCut refinement
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)
cv2.grabCut(img, mask, None, bgdModel, fgdModel, 6, cv2.GC_INIT_WITH_MASK)

# Final mask
fg_mask = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype('uint8')

# Keep only the largest connected component (the person)
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(fg_mask)
if num_labels > 1:
    largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    fg_mask = np.where(labels == largest_label, 255, 0).astype('uint8')

# Fill internal holes (e.g. within glasses or shirt folds)
contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(fg_mask, contours, -1, 255, -1)

# Smooth edges slightly
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

# Make soft alpha edge
blurred_mask = cv2.GaussianBlur(fg_mask, (5, 5), 0)

b, g, r = cv2.split(img)
bgra = cv2.merge([b, g, r, blurred_mask])
cv2.imwrite("scripts/ascii/_work/cutout_clean.png", bgra)
print("Saved clean cutout to scripts/ascii/_work/cutout_clean.png")
