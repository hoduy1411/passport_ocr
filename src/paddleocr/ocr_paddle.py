import cv2
from paddleocr import PaddleOCR

class OCRPaddleReader():
    def __init__(self, cfg_base):
        self.langs = cfg_base["OCR_PADDLE"]["langs"]
        
        self.ocr_models = {lang : PaddleOCR(use_angle_cls=False, lang=lang) for lang in self.langs}
        
    def reader(self, image, lang):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        result = self.ocr_models[lang].ocr(image_rgb, cls=True)
        print(result)

        if len(result):
            text = result[0][0][1][0]
            confidence = result[0][0][1][1]
        
        return text, confidence