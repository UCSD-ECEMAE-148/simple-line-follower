import cv2
import depthai as dai

class BaseCamera():
    def __init__(self, img):
        self.img = img
    def get_frame(self):
        return self.img
    def show_frame():
        pass
    def __del__():
        pass

class ImageCamera(BaseCamera):
    def __init__(self, path='test_images/straight_lines1.jpg', resolution=(300, 300)):
        # load image from path
        self.image = cv2.imread(path)
        self.image = cv2.resize(self.image, resolution)

    def show_frame(self):
        cv2.imshow('frame', self.image)
        
    def get_frame(self):
        return self.image
    
    def __del__(self):
        cv2.destroyAllWindows()

class OAKDCamera(BaseCamera):
    def __init__(self, resolution=(300,300)) -> None:
        self.pipeline = dai.Pipeline()
        self.camRgb = self.pipeline.create(dai.node.ColorCamera)
        self.xoutRgb = self.pipeline.create(dai.node.XLinkOut)
        self.xoutRgb.setStreamName("rgb")
        self.camRgb.setPreviewSize(resolution[0], resolution[1])
        self.camRgb.setInterleaved(False)
        self.camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
        self.camRgb.preview.link(self.xoutRgb.input)
        self.device = dai.Device(self.pipeline)
        self.qRgb = self.device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
        self.frame = None

    def get_frame(self):
        inRgb = self.qRgb.get()
        self.frame = inRgb.getCvFrame()
        return self.frame
    
    def show_frame(self):
        cv2.imshow("rgb", self.frame)
        if cv2.waitKey(1) == ord('q'):
            return False
        return True
    
    def __del__(self):
        cv2.destroyAllWindows()
        self.device.close()
