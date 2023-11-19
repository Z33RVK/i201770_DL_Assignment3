import cv2
import numpy as np
from ultralytics import YOLO

def draw_bbox(event, x, y, flags, param):
    global frame_with_box, drawing, bbox1

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        bbox1 = (x, y, 0, 0)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        bbox1 = (bbox1[0], bbox1[1], x - bbox1[0], y - bbox1[1])
        cv2.rectangle(frame_with_box, (bbox1[0], bbox1[1]), (x, y), (0, 255, 0), 2)
        cv2.imshow('Frame', frame_with_box)

def main():
    # Create a new YOLO model from scratch
    model = YOLO('yolov5s.yaml')

    # Load a pretrained YOLO model (recommended for training)
    model = YOLO('yolov5s.pt')

    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture('Traffic1.mp4')

    # Check if the video file was opened successfully
    if not cap.isOpened():
        print("Error opening video file")

    # Read the first frame
    ret, frame = cap.read()

    # Create a copy of the first frame for drawing the bounding box
    global frame_with_box
    frame_with_box = frame.copy()

    # Initialize variables for bounding box drawing
    global drawing, bbox1
    drawing = False
    bbox1 = (0, 0, 0, 0)

    # Create a window and set the mouse callback
    cv2.namedWindow('Frame')
    cv2.setMouseCallback('Frame', draw_bbox)

    # Display the initial frame with bounding box
    cv2.imshow('Frame', frame_with_box)

    # Wait for 'Enter' key press
    while cv2.waitKey(0) != 13:  # 13 is the ASCII code for 'Enter' key
        pass

    frame_count = 0
    # Play the video from the second frame onwards
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame_count += 1
        print("********Frame Count********: ",frame_count)
        if ret:
            print("*****THE***** bbox length: ",len(bbox1))
            print("*****THE***** bbox contents: ",bbox1)

            # Draw the bounding box on the frame
            #print(bbox)
            print("BBOX_0", bbox1[0])
            print("BBOX_1", bbox1[1])
            print("BBOX_2", bbox1[2])
            print("BBOX_3", bbox1[3])
            cv2.rectangle(frame, (bbox1[0], bbox1[1]), (bbox1[0] - bbox1[2], bbox1[1] - bbox1[3]), (0, 255, 0), 2)
            
            #cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 255, 0), 2)

            # Extract the region of interest (ROI) within the bounding box
            roi = frame[bbox1[1]:bbox1[1] + bbox1[3], bbox1[0]:bbox1[0] + bbox1[2]]

            # Perform object detection on the ROI using YOLO
            if roi.size > 0:  # Check if the ROI is non-empty
                results = model(roi)
                # print(type(results))
                # print(type(results[0]))
                # print(dir(results))
                # print([attr for attr in dir(results) if not attr.startswith('__') and attr != '__class__'])

                bboxes = []
                labels = []
                        
                for result in results:
                    bboxes = result.boxes.numpy()
                    labels = result.names

                    for bbox, name in zip(bboxes, labels):
                        #print("Length of bbox: ",len(bbox))
                        #print("Bbox contents: ",bbox.xyxy)
                        #print(type(bbox.xyxy))
                        if bbox.xyxy.size >= 4:
                            x1, y1, x2, y2 = bbox.xyxy[0]
                            #print(f"Bounding box: ({x1}, {y1}) - ({x2}, {y2}), Name: {name}")
                        else:
                            print("Invalid bounding box format1")

                num_objects = len(bboxes)
                # Draw bounding boxes and labels on the frame if objects are detected
                if num_objects > 0:
                    for bbox in bboxes:
                        if bbox.xyxy.size >= 4:
                            x1, y1, x2, y2 = bbox.xyxy[0]
                            x1, y1, x2, y2 = int(x1.item()), int(y1.item()), int(x2.item()), int(y2.item())
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            roi = frame[y1:y2, x1:x2]
                            # Process the ROI as needed
                        
                            #print(f"Bounding box: ({x1}, {y1}) - ({x2}, {y2})")
                        else:
                            print("Invalid bounding box format2")
                
            # Display the frame with bounding boxes and labels
            cv2.imshow('Frame', frame)
        
            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release the VideoCapture object and close the windows
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()
