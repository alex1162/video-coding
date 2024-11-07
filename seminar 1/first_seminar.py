from PIL import Image    
import numpy as np


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
    
    
class image:
    
    def __init__(self, file_path):  
        self.file_path = file_path
        self.image = Image.open(file_path)

    def resize(self, height, width):
        resized_image = self.image.resize((width, height))
        resized_image.save('resized_image.jpg')
        return resized_image

RGB_color = color(0, 0, 255)

# Convert RGB to YUV
YUV_color = RGB_color.rbg_to_yuv(RGB_color.x, RGB_color.y, RGB_color.z)
print("YUV color:", YUV_color.x, YUV_color.y, YUV_color.z)

# Convert YUV back to RGB
RGB_color = YUV_color.yuv_to_rgb(YUV_color.x, YUV_color.y, YUV_color.z)
print("RGB Color:", RGB_color.x, RGB_color.y, RGB_color.z)

cat = image('olivia.jpg')
resize_cat = cat.resize(500,500)

with open('olivia.jpg', "rb") as image:
  f = image.read()
  b = bytearray(f)
  print (b[0])

