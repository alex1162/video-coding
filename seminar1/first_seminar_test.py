import unittest
import numpy as np
from PIL import Image
from first_seminar import Color, DCT, DWT


class TestColorMethods(unittest.TestCase):
    def test_rgb_to_yuv_and_back(self):
        rgb_color = Color(0, 0, 255)
        yuv_color = rgb_color.rgb_to_yuv(rgb_color.x, rgb_color.y, rgb_color.z)
        self.assertAlmostEqual(yuv_color.x, 41.0, delta=1)
        self.assertAlmostEqual(yuv_color.y, 240.0, delta=1)
        self.assertAlmostEqual(yuv_color.z, 110.0, delta=1)

        rgb_back = yuv_color.yuv_to_rgb(yuv_color.x, yuv_color.y, yuv_color.z)
        self.assertAlmostEqual(rgb_back.x, 1, delta=1)
        self.assertAlmostEqual(rgb_back.y, 0, delta=1)
        self.assertAlmostEqual(rgb_back.z, 255, delta=1)

    def test_rl_encoding_and_decoding(self):
        array = np.array([5, 0, 0, 0, 5, 6, 6, 6, 7, 7, 8])
        encoded = Color.rl_encoding(array)
        self.assertEqual(encoded, [(5, 1), (0, 3), (5, 1), (6, 3), (7, 2), (8, 1)])
        decoded = Color.rl_decoding(encoded)
        self.assertTrue(np.array_equal(array, decoded))

    def test_serpentine(self):
        sample_array = np.array([[1, 2, 3, 4],
                                 [5, 6, 7, 8],
                                 [9, 10, 11, 12],
                                 [13, 14, 15, 16]])
        expected_result = [1, 2, 5, 9, 6, 3, 4, 7, 10, 13, 14, 11, 8, 12, 15, 16]
        serpentine_result = Color.serpentine(sample_array)
        self.assertEqual(serpentine_result, expected_result)

    def test_resize(self):
        input_path = 'olivia.jpg'
        output_path = 'olivia_resized.jpg'
        # Resize the image to 40x40 pixels
        Color.resize_image(input_path, output_path, 40, 40)
        # Verify
        resized_image = Color.load_image_as_matrix(output_path)
        self.assertEqual(np.array(resized_image).shape, (40, 40))

    def test_bw(self):
        input_path = 'olivia.jpg'
        output_path = 'bw_olivia.jpg'
        # Convert the image to black and white (grayscale)
        Color.bw_image(input_path, output_path)
        # Verify if the image is not in color anymore
        bw_image = Color.load_image_as_matrix(output_path)
        self.assertTrue(np.array(bw_image).ndim == 2)

    
class TestDCTMethods(unittest.TestCase):
    def setUp(self):
        self.img_path = 'olivia_resized.jpg'
        self.dct_handler = DCT(self.img_path, 'Q50')
        self.image_array = Color.load_image_as_matrix(self.img_path)

    def test_dct_compression_and_decompression(self):
        compressed_data = self.dct_handler.dct_compression()
        decompressed_image = self.dct_handler.dct_decompression(compressed_data)
        self.assertIsInstance(decompressed_image, Image.Image)
        decompressed_array = np.array(decompressed_image)
        self.assertEqual(decompressed_array.shape, self.image_array.shape)


class TestDWTMethods(unittest.TestCase):
    def setUp(self):
        self.img_path = 'olivia_resized.jpg'
        self.dwt_handler = DWT(self.img_path)

    def test_dwt_compression_and_decompression(self):
        compressed_image, compressed_data = self.dwt_handler.dwt_compression(self.img_path)
        self.assertIsInstance(compressed_image, Image.Image)
        compressed_image.save("dwt_image.png")
        decompressed_image = self.dwt_handler.dwt_decompression(compressed_data)
        self.assertIsInstance(decompressed_image, Image.Image)
        decompressed_image.save("idwt_image.png")
        decompressed_array = np.array(decompressed_image)
        original_array = Color.load_image_as_matrix(self.img_path)
        self.assertEqual(decompressed_array.shape, original_array.shape)


if __name__ == '__main__':
    unittest.main()
