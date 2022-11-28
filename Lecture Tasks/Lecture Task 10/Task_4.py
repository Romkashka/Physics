from matplotlib import pyplot as plt
import cv2
import numpy as np


def create_image(centralized_dft, mask):
    fshift = centralized_dft * mask
    fshift_mask_mag = 20 * np.log(cv2.magnitude(fshift[:, :, 0], fshift[:, :, 1]))
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])
    return fshift_mask_mag, img_back


def handle_image(source):
    img = cv2.imread(source, 0)

    dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
    centralized_dft = np.fft.fftshift(dft)

    magnitude_spectrum = 20 * np.log(cv2.magnitude(centralized_dft[:, :, 0], centralized_dft[:, :, 1]))
    rows, cols = img.shape

    center_x = int(rows / 2)
    center_y = int(cols / 2)
    center = [center_x, center_y]
    x, y = np.ogrid[:rows, :cols]

    mask = np.ones((rows, cols, 2), np.uint8)
    inner_r = 100
    inner_mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= inner_r ** 2
    mask[inner_mask_area] = 0

    mask_outer = np.ones((rows, cols, 2), np.uint8)
    outer_r = 2
    outer_mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= outer_r ** 2
    mask_outer[outer_mask_area] = 0

    img_inner_mask, img1 = create_image(centralized_dft, mask)
    img_outer_mask, img2 = create_image(centralized_dft, mask_outer)

    fig = plt.figure()

    ax1 = fig.add_subplot(3, 2, 1)
    ax1.imshow(img, cmap='gray')

    ax2 = fig.add_subplot(3, 2, 2)
    ax2.imshow(magnitude_spectrum, cmap='gray')

    ax3 = fig.add_subplot(3, 2, 3)
    ax3.imshow(img_inner_mask, cmap='gray')

    ax4 = fig.add_subplot(3, 2, 4)
    ax4.imshow(img1, cmap='gray')

    ax5 = fig.add_subplot(3, 2, 5)
    ax5.imshow(img_outer_mask, cmap='gray')

    ax6 = fig.add_subplot(3, 2, 6)
    ax6.imshow(img2, cmap='gray')

handle_image('images/king.jpg')
handle_image('images/sugavara.jpg')
handle_image('images/ba_dum_tsss.jpg')

plt.show()