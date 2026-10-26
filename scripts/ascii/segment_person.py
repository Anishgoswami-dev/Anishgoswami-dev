import cv2
import numpy as np
from PIL import Image

# Read original photo
img = cv2.imread("input/photo.png")
h, w = img.shape[:2]

# Create a mask initialized to background
mask = np.zeros((h, w), np.uint8)

# The background circle exists outside radius ~185 around center (200, 218)
# Everything outside the circular avatar is definite background
cy, cx = 200, 218
Y, X = np.ogrid[:h, :w]
outside_circle = ((X - cx)**2 + (Y - cy)**2) > (185**2)
mask[outside_circle] = cv2.GC_BGD

# Now define probable background and probable foreground within the circle:
# Background includes:
# - top corners inside circle: Y < 60 or (Y < 120 and (X < 130 or X > 290))
# - sides next to body: (Y > 120 and Y < 220 and (X < 130 or X > 290))
# - ground next to shoulders: (Y >= 220 and (X < 70 or X > 370))
bg_zone = (
    (Y < 50) |
    ((Y < 130) & (X < 140)) |
    ((Y < 130) & (X > 285)) |
    ((Y >= 130) & (Y < 210) & (X < 140)) |
    ((Y >= 130) & (Y < 210) & (X > 280)) |
    ((Y >= 210) & (X < 60)) |
    ((Y >= 210) & (X > 380))
)
mask[bg_zone] = cv2.GC_BGD

# Definite / Probable Foreground:
# Hair & head: Y between 60 and 190, X between 170 and 270
head_zone = (Y >= 65) & (Y <= 190) & (X >= 165) & (X <= 265)
mask[head_zone] = cv2.GC_PR_FGD

# Sunglasses & face center:
face_core = (Y >= 105) & (Y <= 170) & (X >= 175) & (X <= 250)
mask[face_core] = cv2.GC_FGD

# Kurta torso:
kurta_zone = (Y > 210) & (Y < 380) & (X >= 120) & (X <= 320)
mask[kurta_zone] = cv2.GC_FGD

# Run GrabCut
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

cv2.grabCut(img, mask, None, bgdModel, fgdModel, 8, cv2.GC_INIT_WITH_MASK)

# Final mask where foreground is 1
final_mask = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype('uint8')

# Morphological clean up
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_CLOSE, kernel)
final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_OPEN, kernel)

# Apply Gaussian blur for soft edge
# Create 4-channel BGRA image
b, g, r = cv2.split(img)
bgra = cv2.merge([b, g, r, final_mask])

cv2.imwrite("scripts/ascii/_work/cutout_test.png", bgra)
print("Cutout saved to scripts/ascii/_work/cutout_test.png")
