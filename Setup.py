import os
import json
import requests
from google.colab.patches import cv2_imshow
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
from io import BytesIO
%matplotlib inline

import sys

import time
from matplotlib.patches import Polygon


"""
get_text function : calling  API with parameters as image array and some instruction and getting in return the 
text with their coordinates relative to image
"""

def get_text(pathToImage,API_KEY,ENDPOINT):

    print('Processing: ' + pathToImage)

    data = open(pathToImage, 'rb').read()
    
    headers = {'Ocp-Apim-Subscription-Key': API_KEY,
              'Content-Type': 'application/octet-stream'}
    params  = {
            'language': 'en'
            
        }
    response = requests.post(
        ENDPOINT, headers=headers, data=data , params=params)
    response.raise_for_status()
    operation_url = response.headers["Operation-Location"]
    analysis = {}
    poll = True
    while (poll):
        response_final = requests.get(
            response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()

        time.sleep(1)
        if ("recognitionResults" in analysis):
            poll = False
        if ("status" in analysis and analysis['status'] == 'Failed'):
            poll = False

    analysis

    return analysis

"""
get function : Extracting the text from json format and depicating it on top of original images .
"""

def get(analysis,pathToImage):
    
    polygons = []
    if ("recognitionResults" in analysis):
        # Extract the recognized text, with bounding boxes.
        polygons = [(line["boundingBox"], line["text"])
                    for line in analysis["recognitionResults"][0]["lines"]]

    # Display the image and overlay it with the extracted text.
    image = Image.open(pathToImage)
    plt.figure(figsize=(20, 20))
    ax = plt.imshow(image, alpha=0.5)
    
    #Plotting lines on images and writing out the text
    for polygon in polygons:
        vertices = [(polygon[0][i], polygon[0][i+1])
                    for i in range(0, len(polygon[0]), 2)]
        text = polygon[1]
        patch = Polygon(vertices, closed=True, fill=False, linewidth=2, color='y')
        ax.axes.add_patch(patch)
        plt.text(vertices[0][0], vertices[0][1], text, fontsize=20,weight="bold", va="top")

    plt.show()
    return polygons

if __name__ == '__main__':

    parser=argparse.ArgumentParser()
    parser.add_argument('--API_KEY',help='API_KEY')
    parser.add_argument('--DIR',help='address of Directory where input images are saved')
    
    API_KEY =parser.API_KEY 
    DIR = parser.DIR
    pathToImage = DIR

    analysis = get_text(pathToImage)
    polygons = get(analysis,pathToImage)


