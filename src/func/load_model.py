from src.field_detector.field_detector import FieldDetector
from src.ocr.ocr import OCRReader


class LoadModel():
    def __init__(self, cfg_base):
        self.field_detector = FieldDetector(cfg_base)
        self.ocr_reader = OCRReader(cfg_base)