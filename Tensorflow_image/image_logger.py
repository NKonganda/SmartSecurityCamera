from io import StringIO, BytesIO
import subprocess
import os
import time
from datetime import datetime
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

 
# Motion detection settings:
# Threshold (how much a pixel has to change by to be marked as "changed")
# Sensitivity (how many changed pixels before capturing an image)
# ForceCapture (whether to force an image to be captured every forceCaptureTime seconds)
threshold = 10
sensitivity = 20
forceCapture = True
forceCaptureTime = 60 * 60 # Once an hour
 
# File settings
saveWidth = 1280
saveHeight = 960
diskSpaceToReserve = 40 * 1024 * 1024 # Keep 40 mb free on disk
 
# Capture a small test image (for motion detection)
def captureTestImage():
   # command = "raspistill -w %s -h %s -t 0 -e bmp -o -" % (100, 75)
    command = "fswebcam --no-banner -r 1280x720 testimage.jpg"
    imageData = BytesIO()
    imageData.write(subprocess.check_output(command, shell=True))
    imageData.seek(0)
    im = imageData.read()
    im2 = Image.open(imageData)
    buffer = im2.load()
    imageData.close()
    return im2, buffer
 
# Save a full size image to disk
def saveImage(width, height, diskSpaceToReserve):
    keepDiskSpaceFree(diskSpaceToReserve)
    time = datetime.now()
    filename = "capture-%04d%02d%02d-%02d%02d%02d.jpg" % (time.year, time.month, time.day, time.hour, time.minute, time.second)
 #   subprocess.call("raspistill -w 1296 -h 972 -t 0 -e jpg -q 15 -o %s" % filename, shell=True)
    subprocess.call("fswebcam --no-banner -r 1280x720 %s" %filename, shell=True)
    print ("Captured %s") % filename
    # Disable scientific notation for clarity
#     np.set_printoptions(suppress=True)
# 
#     # Load the model
#     model = tensorflow.keras.models.load_model('keras_model.h5')
# 
#     # Create the array of the right shape to feed into the keras model
#     # The 'length' or number of images you can put into the array is
#     # determined by the first position in the shape tuple, in this case 1.
#     data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
# 
#     # Replace this with the path to your image
#     image = Image.open(filename)
# 
#     # resize the image to a 224x224 with the same strategy as in TM2:
#     # resizing the image to be at least 224x224 and then cropping from the center
#     size = (224, 224)
#     image = ImageOps.fit(image, size, Image.ANTIALIAS)
# 
#     # turn the image into a numpy array
#     image_array = np.asarray(image)
# 
#     # display the resized image
#     image.show()
# 
#     # Normalize the image
#     normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
# 
#     # Load the image into the array
#     data[0] = normalized_image_array
# 
#     # run the inference
#     prediction = model.predict(data)
#     print(prediction)

 
    # Keep free space above given level
def keepDiskSpaceFree(bytesToReserve):
    if (getFreeSpace() < bytesToReserve):
        for filename in sorted(os.listdir(".")):
            if filename.startswith("capture") and filename.endswith(".jpg"):
                os.remove(filename)
                print ("Deleted %s to avoid filling disk") % filename
                if (getFreeSpace() > bytesToReserve):
                    return
 
# Get available disk space
def getFreeSpace():
    st = os.statvfs(".")
    du = st.f_bavail * st.f_frsize
    return du
 
# Get first image
image1, buffer1 = captureTestImage()
 
# Reset last capture time
lastCapture = time.time()
 
while (True):
 
    # Get comparison image
    image2, buffer2 = captureTestImage()
 
    # Count changed pixels
    changedPixels = 0
    for x in xrange(0, 100):
        for y in xrange(0, 75):
            # Just check green channel as it's the highest quality channel
            pixdiff = abs(buffer1[x,y][1] - buffer2[x,y][1])
            if pixdiff > threshold:
                changedPixels += 1
 
    # Check force capture
    if forceCapture:
        if time.time() - lastCapture > forceCaptureTime:
            changedPixels = sensitivity + 1
 
    # Save an image if pixels changed
    if changedPixels > sensitivity:
        lastCapture = time.time()
        saveImage(saveWidth, saveHeight, diskSpaceToReserve)
 
    # Swap comparison buffers
    image1 = image2
    buffer1 = buffer2
