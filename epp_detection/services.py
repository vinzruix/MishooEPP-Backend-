from ultralytics import YOLO

model = YOLO("eppmodel/best.pt")


def check_EPP_in_image(image):
    classes = [1, 2, 3, 6, 7]
    results = model(image, classes=classes, conf=0.5, verbose=False, stream=True )

    return results