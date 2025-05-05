import numpy as np
import torch
import sys
sys.path.append("src/yolo")

from src.yolo.models.experimental import attempt_load
from src.yolo.utils.datasets import letterbox
from src.yolo.utils.general import check_img_size, scale_coords, non_max_suppression
from src.yolo.utils.torch_utils import select_device


class FieldDetector():
    def __init__(self, config_base):
        # Initialize
        self.DEVICE = select_device(config_base['DEVICE_TYPE'])
        self.WEIGHTS = config_base['FIELD_PASSPORT_DETECTOR']['WEIGHT']
        self.IMGSZ = config_base['FIELD_PASSPORT_DETECTOR']['IMGSZ']
        self.CONF = config_base['FIELD_PASSPORT_DETECTOR']['CONF']
        self.IOU = config_base['FIELD_PASSPORT_DETECTOR']['IOU']
        self.HALT = self.DEVICE.type != 'cpu'
        self.AGNOSTIC_NMS = True
        self.AUGMENT = False
        self.CLASSES = None

        # Load model
        self.model = attempt_load(self.WEIGHTS, map_location=self.DEVICE)
        self.stride = int(self.model.stride.max())
        self.imgsz = check_img_size(self.IMGSZ, s=self.stride)

        # To FP16
        if self.HALT:
            self.model.half()

        # Get names and colors
        self.names = self.model.names
        
        self.old_img_w = self.old_img_h = self.imgsz
        self.old_img_b = 1

    def predict_image(self, image):
        # Padded resize
        img = letterbox(image, self.imgsz, stride=self.stride)[0]

        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.DEVICE)
        img = img.half() if self.HALT else img.float()
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Warmup
        if self.DEVICE.type != 'cpu' and (self.old_img_b != img.shape[0] or \
                                          self.old_img_h != img.shape[2] or \
                                          self.old_img_w != img.shape[3]):
            self.old_img_b = img.shape[0]
            self.old_img_h = img.shape[2]
            self.old_img_w = img.shape[3]
            for i in range(3):
                self.model(img, augment=self.AUGMENT)[0]

        # Inference
        with torch.no_grad():  # Calculating gradients would cause a GPU memory leak
            pred = self.model(img, augment=self.AUGMENT)[0]

        # Apply NMS
        pred = non_max_suppression(
            pred,
            self.CONF,
            self.IOU,
            classes=self.CLASSES,
            agnostic=self.AGNOSTIC_NMS
        )

        # Process detections
        det = pred[0]

        list_out = []
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], image.shape).round()

            for x1, y1, x2, y2, conf, cls in det.cpu().detach().numpy():
                list_out.append([int(x1),int(y1), int(x2), int(y2), float(conf), int(cls)])

        return list_out