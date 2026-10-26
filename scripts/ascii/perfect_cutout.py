import cv2
import numpy as np

img = cv2.imread("input/photo.png")
h, w = img.shape[:2]

clean = cv2.imread("scripts/ascii/_work/cutout_clean.png", cv2.IMREAD_UNCHANGED)
alpha = clean[:, :, 3].copy()
X_grid, Y_grid = np.meshgrid(np.arange(w), np.arange(h))

# 1. Clean above head: Y < 45
alpha[Y_grid < 45] = 0

# 2. Left of head & face
alpha[(Y_grid >= 45) & (Y_grid <= 70) & (X_grid < 172)] = 0
alpha[(Y_grid > 70) & (Y_grid <= 110) & (X_grid < 166)] = 0

# 3. Left of chin, jaw, and neck:
# Chin is at X=190, neck is at X=195.
# Everything to the left of X=192 for Y in [110, 215] is the pillar/background!
alpha[(Y_grid > 110) & (Y_grid <= 215) & (X_grid < 192)] = 0

# 4. Right of head & hair:
# Hair top right: Y in [45, 75], X > 272 is BG
alpha[(Y_grid >= 45) & (Y_grid <= 75) & (X_grid > 272)] = 0
# Hair middle right: Y in [75, 115], X > 275 is BG
alpha[(Y_grid > 75) & (Y_grid <= 115) & (X_grid > 275)] = 0
# Ear & jawline right: Y in [115, 155], X > 263 is BG
alpha[(Y_grid > 115) & (Y_grid <= 155) & (X_grid > 263)] = 0
# Neck right: Y in [155, 215], X > 250 is BG
alpha[(Y_grid > 155) & (Y_grid <= 215) & (X_grid > 250)] = 0

# 5. Collar & shoulder slopes:
# Left shoulder slopes from (192, 215) down to (80, 290)
# Line: Y - 215 = (290 - 215)/(80 - 192) * (X - 192) = 75 / -112 * (X - 192) = -0.67 * (X - 192)
# Any pixel above this shoulder line is background:
left_shoulder_bg = (Y_grid >= 210) & (Y_grid <= 290) & (X_grid <= 192) & (Y_grid < (215 - 0.67 * (X_grid - 192)))
alpha[left_shoulder_bg] = 0

# Right shoulder slopes from (250, 215) down to (355, 290)
# Line: Y - 215 = (290 - 215)/(355 - 250) * (X - 250) = 75 / 105 * (X - 250) = +0.71 * (X - 250)
right_shoulder_bg = (Y_grid >= 210) & (Y_grid <= 290) & (X_grid >= 250) & (Y_grid < (215 + 0.71 * (X_grid - 250)))
alpha[right_shoulder_bg] = 0

# Left arm outer edge:
alpha[(Y_grid > 290) & (X_grid < 70)] = 0
# Right arm outer edge:
alpha[(Y_grid > 290) & (X_grid > 365)] = 0

# Smooth alpha edge
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, kernel)
alpha = cv2.GaussianBlur(alpha, (3, 3), 0)

clean[:, :, 3] = alpha
cv2.imwrite("scripts/ascii/_work/cutout_perfect.png", clean)
print("Saved scripts/ascii/_work/cutout_perfect.png successfully!")
