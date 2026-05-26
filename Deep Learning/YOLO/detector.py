from ultralytics import YOLO
import cv2
import pandas as pd


model = YOLO('yolov8n.pt')



def detect_image(image):
    results = model(image)

    detections = []

    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls]

            detections.append({
                'Object': label,
                'Confidence': round(conf * 100, 2)
            })

    annotated_image = results[0].plot()

    return annotated_image, pd.DataFrame(detections)
def detect_video(frame):
    results = model(frame)
    annotated_frame = results[0].plot()

    detections = []

    for box in results[0].boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])

        detections.append({
            'Object': model.names[cls],
            'Confidence': round(conf * 100, 2)
        })

    return annotated_frame, pd.DataFrame(detections)