# -*- coding: utf-8 -*-
"""image_classification_test.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cjcrmnwfErh2Rx1mYOhhoHj-XeAumR0c
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os.path
import tensorflow as tf

from urllib.request import urlretrieve
url = ("https://drive.usercontent.google.com/download?id=1mtigz-kMPtI_IJKUmsG_wqNIhuBFUGdu&export=download&authuser=0&confirm=t&uuid=fbe883a9-97f1-4237-8b9f-4aee4712c84e&at=APZUnTVj7nAISG9WUG9QLBkTD_9h%3A1712934384058")
filename = "test.zip"
urlretrieve(url, filename)

!unzip -q test.zip

from google.colab import drive
drive.mount('/content/drive')

loaded_model = tf.keras.models.load_model('/content/drive/My Drive/model_2',compile=True)

class_indices={'baked_potato': 0,
 'baklava': 1,
 'caesar_salad': 2,
 'cheese_sandwich': 3,
 'cheesecake': 4,
 'chicken': 5,
 'chicken_curry': 6,
 'chocolate_cake': 7,
 'donuts': 8,
 'eggs': 9,
 'falafel': 10,
 'fish': 11,
 'french_fries': 12,
 'hamburger': 13,
 'hot_dog': 14,
 'ice_cream': 15,
 'lasagna': 16,
 'omelette': 17,
 'pizza': 18,
 'spaghetti': 19,
 'steak': 20,
 'sushi': 21}

from pathlib import Path
import imghdr
import os

data_dir = "/content/test"
image_extensions = [".png", ".jpg"]

img_type_accepted_by_tf = ["bmp", "gif", "jpeg", "png"]
for filepath in Path(data_dir).rglob("*"):
    if filepath.suffix.lower() in image_extensions:
        img_type = imghdr.what(filepath)
        if img_type is None:
            print(f"{filepath} is not an image")
            os.remove(filepath)
        elif img_type not in img_type_accepted_by_tf:
            print(f"{filepath} is a {img_type}, not accepted by TensorFlow")
            os.remove(filepath)

image_dir=Path('/content/test')
filepaths=list(image_dir.glob(r'**/*.jpg'))
ds_test=pd.DataFrame(filepaths,columns=['Filepath']).astype(str)
ds_test

test_generator=tf.keras.preprocessing.image.ImageDataGenerator(
        preprocessing_function=tf.keras.applications.xception.preprocess_input,
)

test_images=test_generator.flow_from_dataframe(
    dataframe=ds_test,
    x_col='Filepath',
    y_col=None,
    target_size=(299,299),
    color_mode='rgb',
   class_mode=None,
    batch_size=32,
    shuffle=False,
)



predictions=np.argmax(loaded_model.predict(test_images),axis=1)

predictions

def maping_to_cat(x):
     for k,v in class_indices.items():
         if v==x:
             return k

predicted_labels=[maping_to_cat(x) for x in predictions]
predicted_labels

df_temp=pd.DataFrame(predicted_labels,columns=['predicted'])
ds_test=pd.concat([ds_test,df_temp],axis=1)

ds_test

def renameing(x):
   return x.split('/')[-1]
df_test=ds_test.copy()
df_test.Filepath=df_test.Filepath.apply(renameing)
df_test.rename(columns={'Filepath':'name'},inplace=True)
df_test

df_test.to_csv('/content/drive/MyDrive/q1_submission.csv',index=False)

