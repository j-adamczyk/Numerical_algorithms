import cv2
import freetype
import numpy as np
from numpy import rot90, multiply
from numpy.fft import fft2, ifft2
from operator import itemgetter
from pathlib import PurePath
import string
import sys
import test_generator


SIZE = 44


# loads images of characters for chosen font
def load_font_patterns(character_list, font_file):
    face = freetype.Face(font_file)
    face.set_char_size(SIZE * 64)
    result = {}
    for character in character_list:
        face.load_char(character)
        shape = (face.glyph.bitmap.rows, face.glyph.bitmap.width)
        array_np = np.fromiter(face.glyph.bitmap.buffer, dtype=np.ubyte)
        matrix = np.reshape(array_np, shape)
        result[character] = matrix
    return result


# aligns and denoises image
def prepare(image):
    # treshold for image denoising
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # computes rotated bounding box containing text
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    # cv2.minAreaRect returns values in range [-90,0) as the rectangle rotates clockwise angle goes to 0,
    # so we need to add 90 degrees to the angle
    # otherwise, we just take the inverse of the angle to make it positive
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # rotate and align the image
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # again denoising using treshold
    image = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return image


# formats single line for printing (with whitespaces)
def format_line(text, output):
    text.sort(key=itemgetter(0))
    previous_vertical = sys.maxsize
    for char in text:
        # 0.85 factor was chosen empirically
        if char[0] - previous_vertical > int(SIZE * 0.85):
            output += " "
        previous_vertical = char[0]
        output += char[1]
    return output


# formats whole text for printing (with newlines)
def format_text(array):
    text = ""
    previous_horizontal = sys.maxsize
    word = []
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] != 0:
                # factor 0.5 was chosen empirically
                if i - previous_horizontal > int(SIZE * 0.5):
                    text = format_line(word, text)
                    text += "\n"
                    word = []
                previous_horizontal = i
                word += [[j, array[i][j][1]]]
    text = format_line(word, text)
    return text


# removes duplicates (occurrences too close to be separate letters)
def delete_duplicates(array):
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] != 0:
                # factors were chosen empirically
                size1 = int(SIZE * 0.2)
                size2 = int(SIZE * 0.5)
                for k in range(i - size1, i + size1):
                    for l in range(j - size2, j + size2):
                        if (k != i or l != j) and 0 < k < len(array) and len(array[i]) > l > 0 != array[k][l]:
                            if array[k][l][0] > array[i][j][0]:
                                array[i][j][0] = array[k][l][0]
                                array[i][j][1] = array[k][l][1]
                            array[k][l] = 0
    return array


def ocr(text_image, result, characters_images, correlation_factor):
    # text image color inverse
    text_image = 255 - text_image
    w, h = text_image.shape

    # calculate correlations for all letters using FFT
    for character in characters_images:
        # character image is already inversed
        character_image = characters_images[character]

        text_image_FFT = fft2(text_image)
        character_image_FFT = fft2(rot90(character_image, 2), s=(w, h))

        corr = np.abs(ifft2(multiply(text_image_FFT, character_image_FFT))).astype(float)
        max_correlation = np.amax(corr)

        correlation_treshold = correlation_factor * max_correlation

        corr_row, corr_column = corr.shape
        for row in range(corr_row):
            for column in range(corr_column):
                if corr[row, column] >= correlation_treshold:
                    if result[row][column] == 0 or result[row][column][0] < corr[row, column]:
                        result[row][column] = [corr[row, column], character]

        result = delete_duplicates(result)
    return result


# counts recognized characters
def statistics(result, letters, original_text):
    letter_count = len(letters) * [0]
    for i in range(len(result)):
        for j in range(len(letters)):
            if result[i] == letters[j]:
                letter_count[j] += 1
    right_characters = 0
    length = min(len(result), len(original_text))
    for i in range(length):
        if result[i] == original_text[i]:
            right_characters += 1
    return letter_count, right_characters


def main(filename, font, size, original_text):
    font_file = str(PurePath("fonts/" + font + ".ttf"))
    global SIZE
    SIZE = size
    correlation_factor = 0.9

    # rotating and denoising image
    image = cv2.imread(filename)
    image = prepare(image)

    h, w = image.shape

    # setting up results table, it has to account for the letters on the edge
    result = h * [0]
    for x in range(len(result)):
        result[x] = w * [0]

    # get font
    # to search for uppercase, add + string.ascii_uppercase
    # to search for digits, add + string.digits
    characters_list = string.ascii_lowercase + ".,!?"
    characters_images = load_font_patterns(characters_list, font_file)

    # do the actual work
    result = ocr(image, result, characters_images, correlation_factor)
    result = format_text(result)
    print(result)

    occurrences, right_characters = statistics(result, characters_list, text)

    for i in range(len(characters_list)):
        print(characters_list[i] + " occured " + str(occurrences[i]) + " times.")
    print("OCR got " + str(right_characters) + "/" + str(len(original_text)) + " characters right.")


text = "abcde, fghij. klmno! qprst? uwxyz. abcde, fghij. klmno! qprst? uwxyz. abcde, fghij. klmno! qprst? uwxyz."
text_filename = "test_arial"

for size in [12, 30, 50]:
    for font in ["arial", "constantia", "serif", "times_new_roman", "trebuchet", "verdana"]:
        filename = "test_" + str(size) + "_" + font + ".jpg"
        filepath = test_generator.test(filename, font, size, text)
        print("Size: " + str(size) + ", font: " + font)
        main(str(PurePath(filepath)), font, size, text)
