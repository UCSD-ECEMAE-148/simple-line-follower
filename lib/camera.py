import cv2
import depthai as dai
import numpy as np
from utils import JSONManager

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
    def __init__(self, path=None, resolution=(300, 300)):
        # load image from path
        self.image = cv2.imread(path)
        self.image = cv2.resize(self.image, resolution)

    def show_frame(self):
        cv2.imshow('frame', self.image)
        
    def get_frame(self):
        return self.image
    
    def __del__(self):
        cv2.destroyAllWindows()

class OAKDCamera(BaseCamera, JSONManager):
    def __init__(self, resolution=(640,400)) -> None:
        self._camera_config(resolution) # Setup the camera
        self.frame = None

    def _camera_config(self, resolution):
        # Create pipeline
        self.pipeline = dai.Pipeline()

        # Define sources and outputs
        self.monoLeft = self.pipeline.create(dai.node.MonoCamera)
        self.monoRight = self.pipeline.create(dai.node.MonoCamera)
        self.depth = self.pipeline.create(dai.node.StereoDepth)
        self.camRgb = self.pipeline.create(dai.node.ColorCamera)
        self.xoutRgb = self.pipeline.create(dai.node.XLinkOut)
        self.xoutDepth = self.pipeline.create(dai.node.XLinkOut)

        self.xoutRgb.setStreamName("rgb")
        self.xoutDepth.setStreamName("depth")

        # Properties
        self.camRgb.setPreviewSize(resolution[0], resolution[1])
        self.camRgb.setInterleaved(False)
        self.camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
        self.camRgb.preview.link(self.xoutRgb.input)

        self.monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
        self.monoLeft.setCamera("left")
        self.monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
        self.monoRight.setCamera("right")

        # Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
        self.depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
        # Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
        self.depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
        self.depth.setLeftRightCheck(True)
        self.depth.setExtendedDisparity(True)
        self.depth.setSubpixel(True)

        # Linking
        self.monoLeft.out.link(self.depth.left)
        self.monoRight.out.link(self.depth.right)
        self.depth.disparity.link(self.xoutDepth.input)

        self.device = dai.Device(self.pipeline)
        self.device.setIrLaserDotProjectorBrightness(1200) # in mA, 0..1200
        self.device.setIrFloodLightBrightness(1500) # in mA, 0..1500
        self.qRgb = self.device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

    def get_frame(self):
        inRgb = self.qRgb.get()
        self.frame = inRgb.getCvFrame()
        return self.frame
    
    def get_depth(self):
        q = self.device.getOutputQueue(name="depth", maxSize=4, blocking=False)
        inDisparity = q.get()
        frame = inDisparity.getFrame()
        # Normalization for better visualization
        frame = (frame * (255 / self.depth.initialConfig.getMaxDisparity())).astype(np.uint8)
        return frame
    
    def show_frame(self):
        cv2.imshow("rgb", self.frame)
        if cv2.waitKey(1) == ord('q'):
            return False
        return True
    
    def __del__(self):
        cv2.destroyAllWindows()

if __name__ == "__main__":
    import numpy as np
    import cv2

    camera = OAKDCamera()
    print(f'Image shape: {camera.get_frame().shape}, Depth shape: {camera.get_depth().shape}')

    # 1D array gausian kernel
    array = cv2.getGaussianKernel(640, 0)

    # Negate the second half of the array
    array = np.concatenate((array[:320], -array[320:]), axis=0)
    

    while True:
        frame = camera.get_frame()
        depth = camera.get_depth()

        steer = depth @ array
        print(np.sum(steer)/(640*15))

        # Colormap depth map for visualization
        depth = cv2.applyColorMap(depth, cv2.COLORMAP_JET)

        cv2.imshow("rgb", frame)
        cv2.imshow("depth", depth)
        if cv2.waitKey(1) == ord('q'):
            break
