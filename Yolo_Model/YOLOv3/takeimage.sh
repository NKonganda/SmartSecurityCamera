#!/bin/bash
DATE=$(date +"%Y-%m-%d_%H%M")
fswebcam -r 1280x720 --no-banner /home/pi/webcam/Yolo_Model/YOLOv3/photos/$DATE.jpg
