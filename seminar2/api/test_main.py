import unittest
from fastapi.testclient import TestClient
from .main import app  

client = TestClient(app)

class TestFastAPIEndpoints(unittest.TestCase):

    def test_rgb_to_yuv(self):
        response = client.post("/rgb-to-yuv/?R=0&G=0&B=255")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Y", response.json())
        self.assertIn("U", response.json())
        self.assertIn("V", response.json())
        self.assertAlmostEqual(response.json()["Y"], 41.0, delta=1)
        self.assertAlmostEqual(response.json()["U"], 240.0, delta=1)
        self.assertAlmostEqual(response.json()["V"], 110.0, delta=1)

    def test_yuv_to_rgb(self):
        response = client.post("/yuv-to-rgb/?Y=41&U=240&V=110")
        self.assertEqual(response.status_code, 200)
        self.assertIn("R", response.json())
        self.assertIn("G", response.json())
        self.assertIn("B", response.json())
        self.assertAlmostEqual(response.json()["R"], 1, delta=1)
        self.assertAlmostEqual(response.json()["G"], 0, delta=1)
        self.assertAlmostEqual(response.json()["B"], 255, delta=1)

    def test_bw_image(self):
        with open("../media/olivia.jpg", "rb") as file:
            response = client.post("bw-image/", files={"file": file})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertIn("bw_olivia.jpg", response.json()["output_file"])

    def test_resize_image(self):
        with open("../media/olivia.jpg", "rb") as file:
            response = client.post("/resize-image/?width=40&height=40", 
                                   files={"file": file})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertIn("resized_olivia.jpg", response.json()["output_file"])


if __name__ == "__main__":
    unittest.main()
