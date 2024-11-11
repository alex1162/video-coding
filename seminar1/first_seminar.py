import os
import subprocess   
import numpy as np
from PIL import Image
import cv2
from cv2 import *

class color:

    def __init__(self, x, y, z):  
        self.x = x
        self.y = y
        self.z = z
        #self.image = image

    def rbg_to_yuv(self, R, G, B):
        self.x = (( 66 * R + 129 * G +  25 * B + 128) / 256) +  16
        self.y = ((-38 * R -  74 * G + 112 * B + 128) / 256) + 128
        self.z = ((112 * R -  94 * G -  18 * B + 128) / 256) + 128
        return color(self.x, self.y, self.z)
    
    def yuv_to_rgb(self, Y, U, V):
        self.x = 1.164 * (Y-16) + 1.596 * (V-128)
        self.y = 1.164 * (Y-16) - 0.391 * (U-128) - 0.813 * (V-128)
        self.z = 1.164 * (Y-16) + 2.018 * (U-128)

        return color(self.x, self.y, self.z)
    
    @staticmethod #because it belongs to the class, not any instance
    def resize_image(input_path, output_path, width=320, height=240):
        # Command to resize the image using ffmpeg: ffmpeg -i olivia.jpg -vf scale=320:240 output_320x240.png
        command = ['ffmpeg', '-i', input_path,'-vf', f'scale={width}:{height}', output_path]
        subprocess.run(command) 

    @staticmethod
    def serpentine(input_path):

        # TEST WITH ARRAY:
        # input = np.array([[1, 2, 3, 4], 
        #      [5, 6, 7, 8],
        #      [9, 10, 11, 12],
        #      [13, 14, 15, 16]])
        # width, height = input.shape
        # pixels = input.flatten().tolist()
        # 
        # EXPECTED OUTPUT: 1 2 5 9 6 3 4 7 10 13 14 11 8 12 15 16

        # opening image
        image = Image.open(input_path)
        width, height = image.size #dimensions
        pixels = list(image.getdata()) 

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
        for i in range(m * n):
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

    @staticmethod
    def bw_image(input_path, output_path):
        # command: ffmpeg -i input -vf format=gray output
        command = ['ffmpeg', '-i', input_path,'-vf', f'format=gray', output_path]
        subprocess.run(command) 
    
    @staticmethod
    def rl_encoding(bytes):

        # initializing variables
        encoded_bytes = []
        current_byte = bytes[0]
        count = 0

        #loop for every byte in our serie
        for byte in bytes:
            
            if byte == current_byte:
                count += 1
            else:
                encoded_bytes.append((current_byte, count))
                current_byte = byte
                count = 1
    
        # Add the final byte
        encoded_bytes.append((current_byte, count))
        return encoded_bytes

            
## CODE IMPLEMENTATION
RGB_color = color(0, 0, 255)

# Convert RGB to YUV
YUV_color = RGB_color.rbg_to_yuv(RGB_color.x, RGB_color.y, RGB_color.z)
print("YUV color:", YUV_color.x, YUV_color.y, YUV_color.z)

# Convert YUV back to RGB
RGB_color = YUV_color.yuv_to_rgb(YUV_color.x, YUV_color.y, YUV_color.z)
print("RGB Color:", RGB_color.x, RGB_color.y, RGB_color.z)
    
# EXERCISE 3
color.resize_image('olivia.jpg', 'olivia_resized.png', 40, 40)
print('\n')

# EXERCISE 4
serpentine_olivia = color.serpentine('olivia_resized.png')
print(serpentine_olivia)

# EXERCICE 5.1
color.bw_image('olivia.jpg', 'olivia_bw.png')
print('\n')

# EXERCICE 5.2
encoded_serie= color.rl_encoding([5,0,0,0,5,6,6,6,7,7,8])
print(encoded_serie)

from decoder import PyCoefficientDecoder, JDctMethod
filename = 'olivia.jpg'
d = PyCoefficientDecoder(filename, dct_method=JDctMethod.JDCT_FLOAT)
img = d.get_decompressed_image()