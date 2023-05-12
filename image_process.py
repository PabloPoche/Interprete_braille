
import cv2
import imutils
import pickle
import numpy as np
import pandas as pd
from collections import Counter
from keras.models import load_model
from PIL import Image

#model = pickle.load(open('braille_model.pkl', 'rb'))
model = load_model('braille_model.h5') #, compile=False)
#model.compile(optimizer="Adam",
 #             loss='SparseCategoricalCrossentropy',
  #            metrics=['accuracy'])

le = pickle.load(open('braille_encoder.pkl', 'rb'))


def extract_start_end_of_space(hist):
    start= 0
    count= 0
    dfo= pd.DataFrame(columns = ['pixel_value', 'count', 'end', 'start'])
    for i in range(len(hist)-1):
      if hist[i] == 0 :
        count += 1
        if hist[i+1] != 0 or i== 1662:
            d= {'pixel_value': hist[i], 'count':count, 'end': (start + count), 'start': start}
            dfo = pd.concat([dfo, pd.DataFrame(d, index=[0])], ignore_index=True)
            start=(start + count)
      else:
        d= {'pixel_value': hist[i], 'count':1, 'end': (start + 1), 'start': start}
        dfo = pd.concat([dfo, pd.DataFrame(d, index=[0])], ignore_index=True)
        start=(start + 1)
        count= 0
    return dfo

def generate_start_end_text_range(starts, ends):
    start_end= []
    if starts[0] == 0:
      for i in range(len(starts)-1):
          start_end.append((ends[i], starts[i+1]))
    else: 
      ends.append(0)
      for i in range(len(starts)):
          start_end.append((ends[i-1], starts[i]))
    return start_end
  
def find_min_index(df):
    if min(df["start"]) == 0 :
      return min(df["end"])
    else:
      return 0
      
def read_imagen_in_grayscale(inp_img):
    img= cv2.imread(inp_img, cv2.IMREAD_GRAYSCALE)
    return img

def crop_image_prediction(image, model, le):
    resized_img= cv2.resize(image, (28, 28), Image.LANCZOS)
    resized_img= resized_img/255
    resized_img_for_prediction= resized_img.reshape(1, 28,28, 1)
    pred= model.predict(resized_img_for_prediction)
    predictions= le.classes_[pred.argmax(axis=1)]
    print("Prediccion:", predictions)
    return predictions[0]


def process(image):
    gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh_inv= cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    ctrs= cv2.findContours(thresh_inv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ctrs =imutils.grab_contours(ctrs)

    hist= cv2.reduce(thresh_inv.T,1, cv2.REDUCE_AVG).reshape(-1)
    df= extract_start_end_of_space(hist)
    
    bondingBoxes= [list (cv2.boundingRect(c)) for c in ctrs]
    c= Counter([i[2] for i in bondingBoxes])
    mode= c.most_common(1)[0][0]
    if mode > 1 :
      diam= mode
    else:
      diam= c.most_common(2)[1][0]

    df_space= df.loc[ (df["pixel_value"] == 0) & (df["count"] > 4*diam) ]
    space_start_end= [tuple(x) for x in df_space[["start", "end"]].to_records(index=False)]

    starts= [i[0] for i in space_start_end] 
    ends= [i[1] for i in space_start_end]
    text_region_start_end= generate_start_end_text_range(starts, ends)
    
    send_output= []
    for i in range(len(text_region_start_end)):
      text_region= thresh_inv[: ,text_region_start_end[i][0]: text_region_start_end[i][1]+1]
      text_region_orig_image= gray[: ,text_region_start_end[i][0]: text_region_start_end[i][1]+1]
      text_region_hist= cv2.reduce(text_region.T,1, cv2.REDUCE_AVG).reshape(-1)
      df_continous= extract_start_end_of_space(text_region_hist)
      df_spaces= (df_continous.loc[df_continous["pixel_value"] == 0]).reset_index()
      min_index= find_min_index(df_spaces)
      modified_img= text_region_orig_image[: ,min_index:]
      number_of_letters= round(modified_img.shape[1]/diam/4.2)
      splitted_img= np.array_split(modified_img, number_of_letters, axis=1)
      for character in splitted_img:
          word= []
          prediction= crop_image_prediction(character, model, le)
          word.append(prediction)
          send_output.append("".join(word))
      send_output.append(" ")

    print ("Traduccion = {}".format("".join(send_output)))
    return("".join(send_output))