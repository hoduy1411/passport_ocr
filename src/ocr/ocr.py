import torch
import cv2

from PIL import Image
from collections import defaultdict

from src.ocr.tool.config import Cfg
from src.ocr.tool.translate import build_model, translate, translate_beam_search, process_input


class OCRReader():
    def __init__(self, cfg_base):
        self.DEVICE = cfg_base['DEVICE_TYPE']
        self.cfg_model = Cfg.load_config(cfg_base['OCR_CARD']['BASE_CFG'], cfg_base['OCR_CARD']['MODEL_CFG'])
        self.cfg_model['cnn']['pretrained'] = False
        self.cfg_model['predictor']['beamsearch'] = cfg_base['OCR_CARD']['BEAM_SEARCH']
        model, vocab = build_model(self.cfg_model, self.DEVICE)
        weights = self.cfg_model['weights']

        self.return_prob = True
        model.load_state_dict(torch.load(weights, map_location=torch.device(self.DEVICE)))

        self.model = model
        self.vocab = vocab

    def reader(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = process_input(img, self.cfg_model['dataset']['image_height'], 
                self.cfg_model['dataset']['image_min_width'], self.cfg_model['dataset']['image_max_width'])        
        img = img.to(self.DEVICE)

        if self.cfg_model['predictor']['beamsearch']:
            sent = translate_beam_search(img, self.model)
            s = sent
            prob = None
        else:
            s, prob = translate(img, self.model)
            s = s[0].tolist()
            prob = prob[0]

        s = self.vocab.decode(s)
        prob = round(prob, 5)
        
        return s, prob
        
    def predict_batch(self, imgs, return_prob=False):
        bucket = defaultdict(list)
        bucket_idx = defaultdict(list)
        bucket_pred = {}
        
        sents, probs = [0]*len(imgs), [0]*len(imgs)

        for i, img in enumerate(imgs):
            img = process_input(img, self.cfg_model['dataset']['image_height'], 
                self.cfg_model['dataset']['image_min_width'], self.cfg_model['dataset']['image_max_width'])        
        
            bucket[img.shape[-1]].append(img)
            bucket_idx[img.shape[-1]].append(i)


        for k, batch in bucket.items():
            batch = torch.cat(batch, 0).to(self.device)
            s, prob = translate(batch, self.model)
            prob = prob.tolist()

            s = s.tolist()
            s = self.vocab.batch_decode(s)

            bucket_pred[k] = (s, prob)


        for k in bucket_pred:
            idx = bucket_idx[k]
            sent, prob = bucket_pred[k]
            for i, j in enumerate(idx):
                sents[j] = sent[i]
                probs[j] = prob[i]
   
        if return_prob: 
            return sents, probs
        else: 
            return sents