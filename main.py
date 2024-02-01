import cv2
import torch
import os
from time import time
import torchvision.transforms as transforms
from Windowscapture import *
from Classclick import *



os.environ["CUDA_VISIBLE_DEVICES"] = "0"  
# เลือกอุปกรณ์ GPU หรือ CPU 
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
# Load YOLOv7 model
model = torch.hub.load("WongKinYiu/yolov7", "custom", "model/best.pt",force_reload=True)
model = model.to(device)
model.conf =0.4
model.iou = 0.40
# model.classes = 2

loop_time = time()
windowname = 'Heartwood Online'
windows = WindowCapture(windowname)
myclick = Click(windowname)
handle = myclick.gethwid()


while True: 
    screenshot = windows.screenshot()
    # Detect objects using YOLOv5
    results = model(screenshot)
    # Get the bounding boxes of detected objects
    boxes = results.pred[0][:, :4].detach().cpu().numpy()
    # Get the class labels of detected objects
    labels = results.pred[0][:, -1].detach().cpu().numpy()
    # Draw bounding boxes and connect with lines
    for box, label in zip(boxes, labels):
        x1, y1, x2, y2 = box.astype(int)
        class_name = model.names[int(label)]

        object_center_x = (x1 + x2) // 2
        object_center_y = (y1 + y2) // 2
            
        # myclick.control_click(handle,object_center_x,object_center_y-33)
            
        print(f"x={object_center_x}  y ={object_center_y}")
        
        cv2.line(screenshot, (481, 301),  (object_center_x, object_center_y), color=(0, 0, 255), thickness=1)
    
    
        cv2.rectangle(screenshot, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(screenshot, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        

    cv2.imshow('Games', screenshot)
    #print('FPS {}'.format(1 / (time() - loop_time)))
    #loop_time = time()

    # Cv2.waitkey
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    


