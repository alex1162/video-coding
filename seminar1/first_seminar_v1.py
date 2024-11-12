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
        self.x = 1.164 * (Y - 16) + 1.596 * (V - 128)
        self.y = 1.164 * (Y - 16) - 0.391 * (U - 128) - 0.813 * (V - 128)
        self.z = 1.164 * (Y - 16) + 2.018 * (U - 128)
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
    def serpentine(input_array):
        width, height = input_array.shape
        serpentine_pixels = []
        direction = True
        r, c = 0, 0

        for i in range(width * height):
            serpentine_pixels.append(input_array[r][c])
            if direction:
                if r == 0 and c != width - 1:
                    direction = False
                    c += 1
                elif c == width - 1:
                    direction = False
                    r += 1
                else:
                    r -= 1
                    c += 1
            else:
                if c == 0 and r != height - 1:
                    direction = True
                    r += 1
                elif r == height - 1:
                    direction = True
                    c += 1
                else:
                    c -= 1
                    r += 1

        return serpentine_pixels

    @staticmethod
    def rl_encoding(data):
        encoded = []
        count = 1
        current = data[0]
        
        for byte in data[1:]:
            if byte == current:
                count += 1
            else:
                encoded.append((current, count))
                current = byte
                count = 1
        encoded.append((current, count))
        return encoded


class DCT:
    def __init__(self, img_path):
        self.img_path = img_path
        self.image_matrix = None
        self.q_matrix = None
    
    def open_image(self):
        image = Image.open(self.img_path)
        self.image_matrix = np.array(image)
    
    @staticmethod
    def select_q_matrix(level="Q50"):
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
        return matrices.get(level, np.ones((8, 8)))  # Default to a matrix with no compression

    def apply_dct(self):
        self.q_matrix = self.select_q_matrix("Q50")  # Or other chosen quality
        h, w = self.image_matrix.shape
        dct_matrix = np.zeros((h, w))
        
        # Apply DCT on 8x8 blocks
        for i in range(0, h, 8):
            for j in range(0, w, 8):
                block = self.image_matrix[i:i+8, j:j+8] - 128
                dct_block = cv2.dct(block.astype(np.float32))
                quantized_block = np.round(dct_block / self.q_matrix)
                dct_matrix[i:i+8, j:j+8] = quantized_block
        
        return dct_matrix

    def apply_idct(self, dct_matrix):
        h, w = dct_matrix.shape
        decompressed_matrix = np.zeros((h, w))
        
        # Apply IDCT on 8x8 blocks
        for i in range(0, h, 8):
            for j in range(0, w, 8):
                quantized_block = dct_matrix[i:i+8, j:j+8] * self.q_matrix
                idct_block = cv2.idct(quantized_block.astype(np.float32))
                decompressed_matrix[i:i+8, j:j+8] = idct_block + 128
                
        # Convert matrix to an image and save
        img = Image.fromarray(np.clip(decompressed_matrix, 0, 255).astype(np.uint8))
        img.save("output_image.png")

    @staticmethod
    def rl_decoding(encoded_data):
        decoded = []
        for value, count in encoded_data:
            decoded.extend([value] * count)
        return decoded


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

# EXERCISE 6
dct_processor = DCT('olivia_bw.png')
dct_processor.open_image()
compressed_image = dct_processor.apply_dct()
dct_processor.apply_idct(compressed_image)

