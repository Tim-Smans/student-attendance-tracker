import cv2

def is_blurry(img, threshold=100.0):
    laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
    return laplacian_var < threshold
