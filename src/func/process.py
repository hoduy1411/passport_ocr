import cv2
import json

from src.func.correct_data import correct_code, correct_address
from src.func.format_date import format_date
from src.func.format_nation import format_nation_code


def process_image(models, img_path):
    img = cv2.imread(img_path)
    
    # Detect field
    field_boxes = models.field_detector.predict_image(img)
    field_boxes = sorted(field_boxes, key=lambda x: x[1])

    # OCR reader
    payload = {field: {"text": "", "score": 0} for field in models.field_detector.names}

    count_field_name = 0

    for i, box in enumerate(field_boxes):
        name_class = box[5]
        
        if models.field_detector.names[name_class] == "nation":
            img_field = img[box[1]:box[3], box[0]:box[2]]
        else:
            img_field = img[box[1]:box[3], max(0, box[0] - 6):min(box[2] + 6, img.shape[1])]

        s, prob = models.ocr_reader.reader(img_field)
        s = s.upper()

        if payload[models.field_detector.names[name_class]]["text"] == "":
            payload[models.field_detector.names[name_class]] = {
                "text": f'{s}',
                "score": prob    
            }
        else:
            if (models.field_detector.names[name_class] == "name"):
                count_field_name += 1
                if count_field_name < 2:
                    payload[models.field_detector.names[name_class]] = {
                        "text": f'{payload[models.field_detector.names[name_class]]["text"]} {s}',
                        "score": prob
                    }
        
        # Nation code
        if (models.field_detector.names[name_class] == "nation"):
            nation_code = f'{payload[models.field_detector.names[name_class]]["text"]}'
            print('+++++', nation_code)
            payload[models.field_detector.names[name_class]] = {
                "text": f'{format_nation_code(nation_code)}',
                "score": prob
            }

        # Date of birth or Expire date
        if models.field_detector.names[name_class] == "dob":
            print('-=-=', payload[models.field_detector.names[name_class]]["text"])

        if models.field_detector.names[name_class] == "exp":
            print('++--++--', payload[models.field_detector.names[name_class]]["text"])
        
        if (models.field_detector.names[name_class] == "dob") or (models.field_detector.names[name_class] == "exp"):
            date = f'{payload[models.field_detector.names[name_class]]["text"]}'
            #print('-----------', date)
            payload[models.field_detector.names[name_class]] = {
                "text": f'{format_date(date)}',
                "score": prob
            }

        # Draw box
        if (models.field_detector.names[name_class] == "code"):
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 255, 255), 2)
        if (models.field_detector.names[name_class] == "dob"):
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (255, 255, 0), 2)
        if (models.field_detector.names[name_class] == "exp"):
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (255, 0, 255), 2)
        if (models.field_detector.names[name_class] == "nation"):
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)
        if (models.field_detector.names[name_class] == "name"):
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
        if (models.field_detector.names[name_class] == "address"):
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2)
        
    cv2.imwrite(img_path, img)

    # Sort
    payload = {key: payload[key] for key in models.field_detector.names if key in payload}

    # # Correct data
    # payload["nation"]["text"] = correct_code(payload["nation"]["text"])
    
    # if (payload["nation"]["text"] == "VNM"):
    #     payload["address"]["text"] = correct_address(payload["address"]["text"])

    payload = json.dumps(payload, indent=4, ensure_ascii=False)

    return payload


def process_line(models, img_path):
    img = cv2.imread(img_path)
    
    payload = {
        "text": "",
        "score": 0
    }

    # OCR reader
    payload["text"], payload["score"] = models.ocr_reader.reader(img)

    payload = json.dumps(payload, indent=4, ensure_ascii=False)

    return payload