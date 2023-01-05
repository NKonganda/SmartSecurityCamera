import os
import datetime
import sys
import time
import subprocess

script_dir = os.path.dirname(__file__)
os.system("./takeimage.sh")
currentdate = datetime.datetime.now().strftime("%Y-%m-&d_%H%M")
rel_path = currentdate +".jpg"
abs_file_path = os.path.join(script_dir, rel_path)
print(abs_file_path)
