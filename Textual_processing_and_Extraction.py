import os
import numpy as np
from PIL import Image
from io import BytesIO
import sys
import time

def get_details(polygons):  
  Reg=['regn','registration','licence','regn.','no','no.','gn']
  Reg_flag=1
  reg_d=['reg.','regn','from','reon']
  reg_d2=['date of issue']
  reg_d_flag=1
  ch=['ch.','chassis','vin','ch','chasis']
  ch_flag=1
  en=['e','no']
  en2=['engine','eno']
  en_flag=1
  name=["name"]
  name_flag=1
  mfg=['mfg.dt.','dt.','mig.','manufacture','mfg']
  mfg_flag=1
  Regis_no=np.nan
  Regis_date=np.nan
  chassis=np.nan
  engine=np.nan
  name_v=np.nan
  mfg_date=np.nan

  #print(polygons)
  for i,polygon in enumerate(polygons):
      vertices = [(polygon[0][i], polygon[0][i+1])
                  for i in range(0, len(polygon[0]), 2)]
      text = polygon[1]
      text =text.lower()
      text =text.split(' ')
      
      #print(1)
      if ((len(set(Reg).intersection(text))==2)) and Reg_flag and len(text)<7:
        Reg_flag=0
        #print(2)
        if len(polygon[1].split(' ')[-1])>5:
          #print(3)
          if len(polygon[1].split(' ')[-1])>3 :
              #print(4)
              Regis_no=polygon[1].split(' ')[-1]
              continue
          elif len(polygon[1].split(' ')[-2])>3:
              #(5)
              Regis_no=polygon[1].split(' ')[-1]
              continue
        elif len(polygons[i+1][1].split(' ')[-1])>5 and abs(int(vertices[1][0])-int(polygons[i+1][0][0]))<250 and abs(int(vertices[1][1])-int(polygons[i+1][0][1]))<15 and len(polygons[i+1][1].split('/'))==0:
          #print(6)
          if len(polygons[i+1][1].split(' ')[-1])>3 :
              #print(7)
              Regis_no=polygons[i+1][1].split(' ')[-1]
              continue
        elif len(polygon[1].split(' ')[-1])>2 and len(polygon[1].split(' ')[-1])<10:
          #print(8)
          rr=[8,9,10]
          if len(polygon[1].split(' ')[-1]+polygon[1].split(' ')[-2]) in rr:
              #print(9)
              Regis_no=polygon[1].split(' ')[-2]+polygon[1].split(' ')[-1]
              continue
          if text[-1]=='new':
              Regis_no=polygon[1].split(' ')[-2]
              continue

        
      #print(10)
      if ((set(reg_d).intersection(text)) or reg_d2==polygon[1].lower()) and reg_d_flag:
        #print(11)
        reg_d_flag=0
        if reg_d2==text:
          #print(12)
          Regis_date=polygons[i+1][1]
          continue
        else:
          
          if len(text[-1].split('/'))==3:
            Regis_date=polygon[1].split(' ')[-1]
          else:
            Regis_date=polygons[i+1][1].split(' ')[-1]
 
          continue

      if (set(ch).intersection(text)) and ch_flag:
        
        ch_flag=0
        #print(polygon[1].split(' ')[-1])
        if len(polygon[1].split(' ')[-1])>5:
          
          if(len(polygon[1].split(' ')[-1])>10):
            
            chassis=polygon[1].split(' ')[-1]

          else:
            
            chassis=polygon[1].split(' ')[-2]+polygon[1].split(' ')[-1]
        else:
          
          if(len(polygons[i+1][1])>10):
            
            chassis=polygons[i+1][1]
        continue
      
      if ((len(set(en).intersection(text))==2) or (set(en2).intersection(text))) and en_flag:
        
        en_flag=0
        if len(polygon[1].split(' ')[-1])>5:
          
          if(len(polygon[1].split(' ')[-1])>6):
            
            engine=polygon[1].split(' ')[-1]
          else:
            
            engine=polygon[1].split(' ')[-2]+polygon[1].split(' ')[-1]
        
        else:
          
          engine=polygons[i+1][1].split(' ')[-1]
        continue
      
         
      
    
      if (set(name).intersection(text)) and name_flag:
        
        name_flag=0
        
        if abs(int(vertices[1][0])-int(polygons[i+1][0][0]))<250 and abs(int(vertices[1][1])-int(polygons[i+1][0][1]))<15 and len(polygons[i+1][1])>3 and len(polygons[i+1][1])<25:
          
          name_v=polygons[i+1][1]
          continue
        if abs(polygons[i+1][0][2]-polygons[i+2][0][2])<50 and abs(polygons[i+1][0][2]-polygons[i+2][0][2])<8 and len(polygons[i+2][1])>3 and len(polygons[i+2][1])<25:
          
          name_v=polygons[i+2][1]
          continue
        elif abs(int(vertices[1][0])-int(polygons[i+2][0][0]))<250 and abs(int(vertices[1][1])-int(polygons[i+2][0][1]))<15 and len(polygons[i+2][1])>3 and len(polygons[i+2][1])<25:
            
            name_v=polygons[i+2][1]
            continue
        elif len(text)>1:
          for ii,t in enumerate(text):
            if t=='name':
              name_v=polygon[1].split(' ')[ii+1:]
              name_v=' '.join(name_v)
              break

              
        continue
          
      
      if (set(mfg).intersection(text)) and mfg_flag and 'cd' not in text:
        
        
        if len(text[-1].split('/'))>1:
          
          mfg_date=polygon[1].split(' ')[-1]
          mfg_flag=0
        else:
            
            if abs(int(vertices[1][0])-int(polygons[i+1][0][2]))<450 and abs(int(vertices[1][1])-int(polygons[i+1][0][1]))<15:
              if len(polygons[i+1][1].split('/'))>1:
                
                mfg_date=polygons[i+1][1]
                mfg_flag=0
              elif len(polygons[i+2][1].split('/'))>1:
                
                mfg_date=polygons[i+2][1]
                mfg_flag=0

        continue
  
  detail=[Regis_no,Regis_date,chassis,engine,name_v,mfg_date]
  return detail
