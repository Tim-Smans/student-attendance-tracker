from picamera2 import Picamera2

def init_camera():
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (640, 480)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()

    picam2.set_controls({
        "ExposureTime": 8000,
        "AnalogueGain": 3.0,
        "FrameDurationLimits": (10000, 10000),
    })

    return picam2