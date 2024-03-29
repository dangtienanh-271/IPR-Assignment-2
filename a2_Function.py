# a2_Function.py

import cv2
import numpy as np

def apply_filter(image, filter_type='low_pass', cutoff_frequency=0.1):
    if len(image.shape) > 2:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image

    f = np.fft.fft2(gray_image)
    fshift = np.fft.fftshift(f)

    rows, cols = gray_image.shape
    crow, ccol = rows // 2, cols // 2

    mask = np.zeros((rows, cols), np.uint8)
    cutoff_frequency = int(cutoff_frequency * min(rows, cols))  # Convert to integer

    if filter_type == 'low_pass':
        mask[crow - cutoff_frequency:crow + cutoff_frequency, ccol - cutoff_frequency:ccol + cutoff_frequency] = 1
    elif filter_type == 'high_pass':
        mask[crow - cutoff_frequency:crow + cutoff_frequency, ccol - cutoff_frequency:ccol + cutoff_frequency] = 0

    fshift = fshift * mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)

    if len(image.shape) > 2:
        filtered_image = cv2.cvtColor(np.uint8(img_back), cv2.COLOR_GRAY2BGR)
    else:
        filtered_image = np.uint8(img_back)

    return filtered_image
