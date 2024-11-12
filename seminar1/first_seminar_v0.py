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

    def open_image(input_path):
        # opening image
        image = Image.open(input_path)
        width, height = image.size #dimensions
        pixels = list(image.getdata()) 
        return pixels

    @staticmethod
    def serpentine(input):

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


class DCT:
    def __init__(self, img_path, img_mat, q_matrix):
        self.image_path = img_path
        self.image_mat = img_mat
        self.q_matrix = q_matrix

    def open_image(input_path):
        # opening image
        image = Image.open(input_path)
        width, height = image.size #dimensions
        pixels = list(image.getdata()) 
        return pixels

    @staticmethod
    def serpentine(input):

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
    
    @staticmethod
    def rl_decoding(compressed_seq: list) -> list:
        decoded_seq = []

        # Iterate over the compressed sequence, taking two elements at a time (count, value)
        for i in range(0, len(compressed_seq), 2):
            count = compressed_seq[i]
            value = compressed_seq[i + 1]
            
            # Extend the decoded sequence with 'count' occurrences of 'value'
            decoded_seq.extend([value] * count)
            
        return decoded_seq


    @staticmethod
    def bw_image(self, input_path, output_path):
        # command: ffmpeg -i input -vf format=gray output
        command = ['ffmpeg', '-i', input_path,'-vf', f'format=gray', output_path]
        subprocess.run(command) 
        self.image_path = output_path
    
    @staticmethod
    def mat_image(self, input_path):
        # opening image
        image = Image.open(input_path)
        width, height = image.size #dimensions
        pixels = list(image.getdata()) 

        # creating matrix with pixel values
        mat = [pixels[i * width:(i + 1) * width] for i in range(height)]
        self.image_mat = mat
    
    @staticmethod
    def mapped_dct(self):
        mat = self.image_mat
        height = len(mat)
        width = len(mat[0])

        for i in range(0, height):
            for j in range(0, width):
                mat[i][j] -= 128
        
        return mat
    
    @staticmethod
    def mapped_idct(self):
        mat = self.image_mat
        height = len(mat)
        width = len(mat[0])

        for i in range(0, height):
            for j in range(0, width):
                mat[i][j] += 128
        
        return mat
    
    #Quantization Arrays
    @staticmethod
    def selectQMatrix(self, qName):
        Q10 = np.array([[80,60,50,80,120,200,255,255],
                    [55,60,70,95,130,255,255,255],
                    [70,65,80,120,200,255,255,255],
                    [70,85,110,145,255,255,255,255],
                    [90,110,185,255,255,255,255,255],
                    [120,175,255,255,255,255,255,255],
                    [245,255,255,255,255,255,255,255],
                    [255,255,255,255,255,255,255,255]])

        Q50 = np.array([[16,11,10,16,24,40,51,61],
                    [12,12,14,19,26,58,60,55],
                    [14,13,16,24,40,57,69,56],
                    [14,17,22,29,51,87,80,62],
                    [18,22,37,56,68,109,103,77],
                    [24,35,55,64,81,104,113,92],
                    [49,64,78,87,103,121,120,101],
                    [72,92,95,98,112,100,130,99]])

        Q90 = np.array([[3,2,2,3,5,8,10,12],
                        [2,2,3,4,5,12,12,11],
                        [3,3,3,5,8,11,14,11],
                        [3,3,4,6,10,17,16,12],
                        [4,4,7,11,14,22,21,15],
                        [5,7,11,13,16,12,23,18],
                        [10,13,16,17,21,24,24,21],
                        [14,18,19,20,22,20,20,20]])
        if qName == "Q10":
            self.q_matrix = Q10
        elif qName == "Q50":
            self.q_matrix = Q50
        elif qName == "Q90":
            self.q_matrix = Q90
        else:
            self.q_matrix = np.ones((8, 8)) # we return the original image back
    
    @staticmethod
    def dct_compression(self):
        mat_bw = self.image_mat
        height = len(mat_bw)
        width = len(mat_bw[0])

        dct_mat = [[0 for _ in range(height)] for _ in range(width)]

        mapped_mat = mat_bw.mapped_dct()

        N = 8

        q_matrix = self.selectQMatrix("Q10")

        # we will create a grid of blocks of 8x8 pixels

        # iterating over each 8x8 block
        for i in range(0, height, N):
            for j in range(0, width, N):

                # here we have the pixels for one 8x8 block
                for x in range(i, i + N):
                    for y in range(j, j + N):

                        # now we will compute the DCT following the matrix multiplication: D = TMT'
                        t_mat = [[0 for _ in range(8)] for _ in range(8)]

                        if x == 0:
                            t_mat[x][y] = 1/np.sqrt(N)
                        
                        elif x > 0:
                            t_mat[x][y] = np.sqrt(2/N) * np.cos(((2j+1)*i*np.pi)/(2*N))
                        
                        d_mat = np.dot(np.dot(t_mat, mapped_mat), t_mat.T)

                        dct_mat[i + x, j + y] = np.around(d_mat[x,y]/q_matrix[x,y])

                        pixels = self.serpentine(dct_mat)

                        img_encoded = self.rl_encoding(pixels)

        return img_encoded
    
    @staticmethod
    def dct_decompression(self, img_encoded):
        array = self.rl_decoding(img_encoded)
        width, height = array.shape
        pixels = list(array.getdata()) 

        # creating matrix with pixel values
        mat = [pixels[i * width:(i + 1) * width] for i in range(height)]

        N = 8

        q_matrix = self.selectQMatrix("Q10")

        # we will create a grid of blocks of 8x8 pixels

        # iterating over each 8x8 block
        for i in range(0, height, N):
            for j in range(0, width, N):
                # R = Q x C
                r_mat = np.dot(q_matrix, mat[i : (i + N), j : (j + N)])
        
        final_mat = cv2.idct(r_mat).mapped_idct()

        # Convert the matrix to a PIL Image
        img = Image.fromarray(final_mat)

        # Save the image as PNG
        img.save("output_image.png")


## CODE IMPLEMENTATION

# EXERCISE 1
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
encoded_message= color.rl_encoding([5,0,0,0,5,6,6,6,7,7,8])
print(encoded_message)