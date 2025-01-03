from ultralytics import YOLO

class customYOLO(YOLO):
    def __init__(self, model, task=None, verbose=False):
        super().__init__(model, task, verbose)

if __name__ == '__main__':
    model = customYOLO("custom_yolov8s.pt")