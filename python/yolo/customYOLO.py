from ultralytics import YOLO

class customYOLO(YOLO):
    def __init__(self, model, task=None, verbose=False):
        super().__init__(model, task, verbose)
    
    def __call__(self, source = None, stream = False, **kwargs):
        result = super().__call__(source, stream, **kwargs)[0]
        
        return result.plot()


if __name__ == '__main__':
    model = customYOLO("custom_yolov8s.pt")