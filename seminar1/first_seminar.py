import os
import subprocess   
import numpy as np
from PIL import Image
import cv2
import pywt
import unittest


class Color:
    def __init__(self, x, y, z):  
        self.x = x
        self.y = y
        self.z = z
    
    # to change pixels from RGB to YUV
    def rgb_to_yuv(self, R, G, B):
        self.x = ((66 * R + 129 * G + 25 * B + 128) / 256) + 16
        self.y = ((-38 * R - 74 * G + 112 * B + 128) / 256) + 128
        self.z = ((112 * R - 94 * G - 18 * B + 128) / 256) + 128
        return Color(self.x, self.y, self.z)
    
    # to change pixels from RGB to YUV
    def yuv_to_rgb(self, Y, U, V):
        self.x = 1.164 * (Y-16) + 1.596 * (V-128)
        self.y = 1.164 * (Y-16) - 0.391 * (U-128) - 0.813 * (V-128)
        self.z = 1.164 * (Y-16) + 2.018 * (U-128)
        return Color(self.x, self.y, self.z)

    # we have created this method to be used later on when reading images
    @staticmethod
    def load_image_as_matrix(img_path):
        image = Image.open(img_path).convert('L')
        return np.array(image)

    # resizing the image using ffmpeg command
    @staticmethod
    def resize_image(input_path, output_path, width=320, height=240):
        command = ['ffmpeg', '-i', input_path, '-vf', f'scale={width}:{height}', output_path]
        subprocess.run(command)

    # turning the image to black & white using ffmpeg command
    @staticmethod
    def bw_image(input_path, output_path):
        command = ['ffmpeg', '-i', input_path, '-vf', 'format=gray', output_path]
        subprocess.run(command)

    # method to do rl encoding
    @staticmethod
    def rl_encoding(values_seq):
        encoded_values = []
        current_byte = values_seq[0]
        count = 0
        for byte in values_seq:
            if byte == current_byte:
                count += 1
            else:
                encoded_values.append((current_byte, count))
                current_byte = byte
                count = 1
        encoded_values.append((current_byte, count))
        return encoded_values

    # we have created another method to decode the rl_encoding
    @staticmethod
    def rl_decoding(encoded_seq):
        decoded_seq = []
        for value, count in encoded_seq:
            decoded_seq.extend([value] * count)
        return np.array(decoded_seq)

    @staticmethod
    def serpentine(matrix):
        # TEST WITH ARRAY:
        # input = np.array([[1, 2, 3, 4], 
        #      [5, 6, 7, 8],
        #      [9, 10, 11, 12],
        #      [13, 14, 15, 16]])
        # 
        # EXPECTED OUTPUT: 1 2 5 9 6 3 4 7 10 13 14 11 8 12 15 16

        width, height = input.shape
        pixels = input.flatten().tolist()

        # creating matrix with pixel values
        mat = [pixels[i * width:(i + 1) * width] for i in range(height)]

        # initializing variables
        r = 0 # rows
        c = 0 # columns
        m = width
        n = height
        serpentine_pixels = []
        direction = True

        # loop for all pixels
        for _ in range(m * n):
            serpentine_pixels.append(mat[r][c]) # add pixel to the list

            # up-right direction
            if direction:
                # top row but not last col-> change direction and move right
                if r == 0 and c != n-1:
                    direction = False
                    c += 1 
                # last col-> change direction and move down
                elif c == n-1:
                    direction = False
                    r += 1 
                # continue moving up-right
                else:
                    r -= 1 
                    c += 1 

            # down-left direction
            else:
                # first col but not las row-> change direction and move down
                if c == 0 and r != m-1:
                    direction = True
                    r += 1 
                # last row-> change direction and move right
                elif r == m-1:
                    direction = True
                    c += 1 
                # continue moving down-left
                else:
                    c -= 1
                    r += 1 

        return serpentine_pixels


class DCT:
    def __init__(self, img_path, q_matrix_level):
        self.img_path = img_path
        self.q_matrix_level = q_matrix_level
        self.image_mat = Color.load_image_as_matrix(img_path)

    def select_q_matrix(self, level="Q50"):
        matrices = {
            "Q10": np.array([[80,60,50,80,120,200,255,255],
                    [55,60,70,95,130,255,255,255],
                    [70,65,80,120,200,255,255,255],
                    [70,85,110,145,255,255,255,255],
                    [90,110,185,255,255,255,255,255],
                    [120,175,255,255,255,255,255,255],
                    [245,255,255,255,255,255,255,255],
                    [255,255,255,255,255,255,255,255]]),  

            "Q50": np.array([[16,11,10,16,24,40,51,61],
                    [12,12,14,19,26,58,60,55],
                    [14,13,16,24,40,57,69,56],
                    [14,17,22,29,51,87,80,62],
                    [18,22,37,56,68,109,103,77],
                    [24,35,55,64,81,104,113,92],
                    [49,64,78,87,103,121,120,101],
                    [72,92,95,98,112,100,130,99]]),    

            "Q90": np.array([[3,2,2,3,5,8,10,12],
                        [2,2,3,4,5,12,12,11],
                        [3,3,3,5,8,11,14,11],
                        [3,3,4,6,10,17,16,12],
                        [4,4,7,11,14,22,21,15],
                        [5,7,11,13,16,12,23,18],
                        [10,13,16,17,21,24,24,21],
                        [14,18,19,20,22,20,20,20]])
        }
        
        return matrices.get(level, np.ones((8, 8)))

    def dct_compression(self):
        height, width = self.image_mat.shape
        dct_transformed = np.zeros_like(self.image_mat, dtype=np.float32) 
        q_matrix = self.select_q_matrix(self.q_matrix_level)
        N = 8 # because we want 8x8 blocks

        for i in range(0, height, N):
            for j in range(0, width, N):
                block = self.image_mat[i:i+N, j:j+N]   # centering pixel values around zero
                dct_block = cv2.dct(np.float32(block))
                quantized_block = np.round(dct_block / q_matrix).astype(int)
                dct_transformed[i:i+N, j:j+N] = quantized_block

        encoded_data = Color.rl_encoding(dct_transformed.flatten())
        return encoded_data

    def dct_decompression(self, encoded_data):
        decoded_data = Color.rl_decoding(encoded_data)
        height, width = self.image_mat.shape
        decompressed_image = np.zeros((height, width), dtype=np.uint8)
        q_matrix = self.select_q_matrix(self.q_matrix_level)
        N = 8

        reshaped_data = np.reshape(decoded_data, (height, width))
        for i in range(0, height, N):
            for j in range(0, width, N):
                quantized_block = reshaped_data[i:i+N, j:j+N]
                dequantized_block = quantized_block * q_matrix
                idct_block = cv2.idct(dequantized_block) 
                decompressed_image[i:i+N, j:j+N] = np.clip(idct_block, 0, 255)

        return Image.fromarray(decompressed_image)


class DWT:
    def __init__(self, img_path):
        self.img_path = img_path
    
    def dwt_compression(self, img_path):
        image = np.array(Image.open(img_path).convert('L')) # obtaining the array of values of the image in bw
        dwt = pywt.dwt2(image, 'sym4') #coefficients
        cA, (cH, cV, cD) = dwt
        
        # combining the coefficients to form a single image for visualization
        transformed_array = np.vstack((
            np.hstack((cA, cH)),
            np.hstack((cV, cD))
        ))
        
        return Image.fromarray(np.uint8(np.clip(transformed_array, 0, 255))), dwt
    
    def dwt_decompression(self, compressed_data):
        data = pywt.idwt2(compressed_data, 'sym4')
        
        return Image.fromarray(np.uint8(np.clip(data, 0, 255)))

# UNIT TESTS

# Exercise 1
rgb_color = Color(0, 0, 255)
yuv_color = rgb_color.rgb_to_yuv(rgb_color.x, rgb_color.y, rgb_color.z)
print("YUV Color:", yuv_color.x, yuv_color.y, yuv_color.z)
rgb_back = yuv_color.yuv_to_rgb(yuv_color.x, yuv_color.y, yuv_color.z)
print("RGB Color:", rgb_back.x, rgb_back.y, rgb_back.z)

# Exercise 3
Color.resize_image('olivia.jpg', 'olivia_resized.png', 480, 320)

# Exercise 4
sample_array = np.random.randint(0, 255, (8, 8))
serpentine_result = Color.serpentine(sample_array)
print("Serpentine Pattern:", serpentine_result)

# Exercise 5.1
Color.bw_image('olivia_resized.png', 'olivia_bw.png')

# Exercise 5.2
encoded_result = Color.rl_encoding(np.array([5, 0, 0, 0, 5, 6, 6, 6, 7, 7, 8]))
print("Run-Length Encoded:", encoded_result)
decoded_result = Color.rl_decoding(encoded_result)
print("Run-Length Decoded:", decoded_result)

# Exercise 6
img_path = 'olivia_bw.png'
dct_handler = DCT(img_path, 'Q90')
compressed_data = dct_handler.dct_compression()
decompressed_image = dct_handler.dct_decompression(compressed_data)
decompressed_image.save("output_image.png")

# Exercise 7
img_path = 'olivia_bw.png'
dwt_image = DWT(img_path)
compressed_data = dwt_image.dwt_compression(img_path)
compressed_data[0].save("dwt_image.png")
decompressed_data = dwt_image.dwt_decompression(compressed_data[1])
decompressed_data.save("idwt_image.png")