import os
import subprocess   
import numpy as np
from PIL import Image
import cv2

class Color:
    def __init__(self, x, y, z):  
        self.x = x
        self.y = y
        self.z = z

    def rgb_to_yuv(self, R, G, B):
        self.x = ((66 * R + 129 * G + 25 * B + 128) / 256) + 16
        self.y = ((-38 * R - 74 * G + 112 * B + 128) / 256) + 128
        self.z = ((112 * R - 94 * G - 18 * B + 128) / 256) + 128
        return Color(self.x, self.y, self.z)
    
    def yuv_to_rgb(self, Y, U, V):
        self.x = 1.164 * (Y-16) + 1.596 * (V-128)
        self.y = 1.164 * (Y-16) - 0.391 * (U-128) - 0.813 * (V-128)
        self.z = 1.164 * (Y-16) + 2.018 * (U-128)
        return Color(self.x, self.y, self.z)

    @staticmethod
    def resize_image(input_path, output_path, width=320, height=240):
        command = ['ffmpeg', '-i', input_path, '-vf', f'scale={width}:{height}', output_path]
        subprocess.run(command)

    @staticmethod
    def bw_image(input_path, output_path):
        command = ['ffmpeg', '-i', input_path, '-vf', 'format=gray', output_path]
        subprocess.run(command)

    @staticmethod
    def rl_encoding(bytes_seq):
        encoded_bytes = []
        current_byte = bytes_seq[0]
        count = 0
        for byte in bytes_seq:
            if byte == current_byte:
                count += 1
            else:
                encoded_bytes.append((current_byte, count))
                current_byte = byte
                count = 1
        encoded_bytes.append((current_byte, count))
        return encoded_bytes

    @staticmethod
    def serpentine(matrix):
        rows, cols = matrix.shape
        serpentine_pixels = []
        direction = True
        r, c = 0, 0

        for _ in range(rows * cols):
            serpentine_pixels.append(matrix[r][c])
            if direction:
                if r == 0 and c != cols - 1:
                    direction = False
                    c += 1
                elif c == cols - 1:
                    direction = False
                    r += 1
                else:
                    r -= 1
                    c += 1
            else:
                if c == 0 and r != rows - 1:
                    direction = True
                    r += 1
                elif r == rows - 1:
                    direction = True
                    c += 1
                else:
                    r += 1
                    c -= 1
        return serpentine_pixels


class DCT:
    def __init__(self, img_path, q_matrix_level):
        self.img_path = img_path
        self.q_matrix_level = q_matrix_level
        self.image_mat = self.load_image_as_matrix(img_path)

    @staticmethod
    def load_image_as_matrix(img_path):
        image = Image.open(img_path).convert('L')
        return np.array(image)

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
        N = 8

        for i in range(0, height, N):
            for j in range(0, width, N):
                block = self.image_mat[i:i+N, j:j+N] - 128  # Center pixel values around zero
                dct_block = cv2.dct(np.float32(block))
                quantized_block = np.round(dct_block / q_matrix).astype(int)
                dct_transformed[i:i+N, j:j+N] = quantized_block

        serpentine_order = Color.serpentine(dct_transformed)
        encoded_data = Color.rl_encoding(serpentine_order)
        return encoded_data

    def dct_decompression(self, encoded_data):
        decoded_data = self.rl_decoding(encoded_data)
        height, width = self.image_mat.shape
        decompressed_image = np.zeros((height, width), dtype=np.uint8)
        q_matrix = self.select_q_matrix(self.q_matrix_level)
        N = 8

        reshaped_data = np.reshape(decoded_data, (height, width))
        for i in range(0, height, N):
            for j in range(0, width, N):
                quantized_block = reshaped_data[i:i+N, j:j+N]
                dequantized_block = quantized_block * q_matrix
                idct_block = cv2.idct(dequantized_block + 128)
                decompressed_image[i:i+N, j:j+N] = np.clip(idct_block, 0, 255)

        return Image.fromarray(decompressed_image)

    @staticmethod
    def rl_decoding(encoded_seq):
        decoded_seq = []
        for value, count in encoded_seq:
            decoded_seq.extend([value] * count)
        return np.array(decoded_seq)


# EXAMPLES OF EXERCISES

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

# EXERCICE 5.1
Color.bw_image('olivia_resized.png', 'olivia_bw.png')
print('\n')

# Exercise 5.2
encoded_result = Color.rl_encoding([5, 0, 0, 0, 5, 6, 6, 6, 7, 7, 8])
print("Run-Length Encoded:", encoded_result)

# Exercise 6
img_path = 'olivia_bw.png'
dct_handler = DCT(img_path, 'Q50')
compressed_data = dct_handler.dct_compression()
decompressed_image = dct_handler.dct_decompression(compressed_data)
decompressed_image.save("output_image.png")