from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import cv2

class customYOLO(YOLO):
    def __init__(self, model, task=None, verbose=False):
        super().__init__(model, task, verbose)
        self.results = list()
        self.CONFIDENCE_THRESHOLD = 0.8
    
    def __call__(self, source = None, stream = False, **kwargs):
        result = super().__call__(source, stream, **kwargs)[0]
        
        for data in result.boxes.data.tolist():
            confidence = data[4]
            if confidence < self.CONFIDENCE_THRESHOLD:
                continue

            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            class_id = int(data[5])

            self.results.append([[xmin, ymin, xmax - xmin, ymax - ymin], confidence, class_id])

        return self.results
    
def tracking(tracker, results, frame):
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)

    tracks = tracker.update_tracks(results, frame=frame)
    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        ltrb = track.to_ltrb()

        xmin, ymin, xmax, ymax = int(ltrb[0]), int(ltrb[1]), int(ltrb[2]), int(ltrb[3])

        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), GREEN, 2)
        cv2.rectangle(frame, (xmin, ymin - 20), (xmin + 20, ymin), GREEN, -1)
        cv2.putText(frame, str(track_id), (xmin + 5, ymin - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)
    
    return frame
