import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def load_image(filename):
    matrix = np.asarray(Image.open(filename))
    return matrix


def low_rank_approximation(matrix, k):
    U, S, V = np.linalg.svd(matrix)
    Uk = np.matrix(U[:, :k])
    Sk = np.diag(S[:k])
    Vk = np.matrix(V[:k, :])
    result = Uk * Sk * Vk
    return result


def get_quality(matrix, approx_matrix):
    diff_matrix = np.subtract(matrix, approx_matrix)
    quality = np.linalg.norm(diff_matrix)
    return quality


matrix = load_image("lenna_image_512.jpg")

ks = []
qualities = []

images = []

for k in range(512, 31, -32):
    approx_matrix = low_rank_approximation(matrix, k)
    ks.append(k)
    quality = get_quality(matrix, approx_matrix)
    qualities.append(quality)
    compressed_image = Image.fromarray(approx_matrix)
    compressed_image = compressed_image.convert("RGB")
    images.append(compressed_image)
    filename = "img/lenna_image_" + str(k) + ".jpg"
    compressed_image.save(filename)

plt.plot(ks, qualities)
plt.show()

images[0].save("lennas.gif", save_all=True, append_images=images[1:], duration=256, loop=0)
