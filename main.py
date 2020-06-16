import collections
import pandas as pd
import os
import json
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import sys
import time
import parser

from Setup import handler
from Setup import get_text
from Textual_processing_and_Extraction  import get_details



def handler(API_KEY,ENDPOINT = 'https://cvisionai.cognitiveservices.azure.com/vision/v2.1/read/core/asyncBatchAnalyze',DIR):
    count=0
    text = ''
    details=[]
    for filename in sorted(os.listdir(DIR)):
        if filename.endswith(".jpg"):
            count=count+1 
            pathToImage = '{0}/{1}'.format(DIR, filename)
            img=cv2.imread(pathToImage)
            #cv2_imshow(img)
            if count%5==0:
              
              time.sleep(30)
            analysis = get_text(pathToImage)
            polygons=get(analysis,pathToImage)
            detail=get_details(polygons)
            detail.insert(0,filename)
            details.append(detail)
    
    return details,analysis,polygons


def resize(read_path,output_path):  
  image=cv2.imread(read_path)
  (h,w,_)=image.shape
  print(image.shape[:2])
  r=w/h
  newh=(int((r*1200)/32)*32)
  dim=(int(newh),int(1200))
  image=cv2.resize(image,dim)
  cv2.imwrite(output_path,image)



class OrderedSet(collections.Set):
    def __init__(self, iterable=()):
        self.d = collections.OrderedDict.fromkeys(iterable)

    def __len__(self):
        return len(self.d)

    def __contains__(self, element):
        return element in self.d

    def __iter__(self):
        return iter(self.d)
 
def Save_result(details):

    df=pd.DataFrame(columns=['filename','Regn no' , 'Registration date','Chassis','Engine no','Name','Mfg. date'])
    
    f=[':']
    new_details=[]

    for detail in details:
        fields=[]
        for field in detail:
            if type(field)==np.float:
                field=str(field)
            print(field)
            field=field.split(' ')
            field=OrderedSet(field)-OrderedSet(f)
            field=' '.join(field)
            fields.append(field)

        new_details.append(fields)


    for i,detail in enumerate(new_details):
        df.loc[i]=detail

    df.to_csv('Final.csv', sep=',')


if __name__ == '__main__':

    parser=argparse.ArgumentParser()
    parser.add_argument('--API_KEY',help='API_KEY')
    parser.add_argument('--DIR',help='address of Directory where input images are saved')
    
    API_KEY =parser.API_KEY 
    DIR = parser.DIR
    
    # resizing all images 
    filenames=os.listdir(DIR)
    for filename in filenames:
        read_path='./'+str(DIR)+"/"+filename   # relative to your previous path enter folder in which images are savedd
        output_path='./rc4/'+filename  
        resize(read_path,output_path)

    details,analysis,polygons=handler(API_KEY,ENDPOINT,DIR)
    

    #saving in .txt format
    with open('details.txt', 'w') as outfile:
      json.dump(details, outfile)  

    #saving in csv format
    Save_result(details)
    
    


