import matplotlib.pyplot as plt
import numpy as np
from numpy import fft, rot90, multiply
from PIL import Image


img = np.asarray(Image.open("school_of_fish.png").convert("L"))

school_of_fish = np.zeros((img.shape[0], img.shape[1]))
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        school_of_fish[i, j] = img[i, j][0]  # getting R channel

school_of_fish = fft.fft2(school_of_fish)

# plot absolutes
absolute_matrix = np.log10(np.abs(school_of_fish)).astype(np.float64)  # log scale, since without it the image will be entirely black
plt.imshow(absolute_matrix, cmap="gray")
plt.show()

# plot phases
phase_matrix = np.angle(school_of_fish)
plt.imshow(phase_matrix, cmap="gray")
plt.show()


fish = np.asarray(Image.open("fish.png").convert("L"))
fish_x = fish.shape[0]
fish_y = fish.shape[1]
w, h = school_of_fish.shape
fish = fft.fft2(rot90(fish, 2), s=(w, h))

absolute_correlations = abs(fft.ifft2(multiply(school_of_fish, fish)))
max_correlation = np.amax(absolute_correlations)

new_img = np.array(Image.open("school_of_fish.png").convert("RGB"))

for i in range(absolute_correlations.shape[0]):
    for j in range(absolute_correlations.shape[1]):
        if absolute_correlations[i, j] >= 0.5 * max_correlation:
            new_img[i, j][0] = 200

result = Image.fromarray(new_img)
result.save("new_school_of_fish.jpg")
