import keras.backend as K
import keras
from keras import layers, activations
from keras.models import Model
from keras.preprocessing.image import load_img,img_to_array
from keras.utils.vis_utils import plot_model
from keras.engine.topology import Layer

def small_Unet(labels=1,h=128,w=128, out_activation = "sigmoid"): # here we have the width and hight are 128 bec we had resized our image
    
    class MySoftmax(Layer):
        #http://cookie-box.hatenablog.com/entry/2017/08/15/231503 
        def __init__(self, **kwargs):
            super(MySoftmax, self).__init__(**kwargs)
        def call(self, x):
            return(activations.softmax(x, axis=3))

    
    
    #block1, 128x128
    inputs = layers.Input(shape=(h,w,3))
    conv11 = layers.Conv2D(16,(3,3),activation="relu",padding="same")(inputs) # (3,3) is the kernal size 
    conv12= layers.Conv2D(16,(3,3),activation="relu",padding="same")(conv11) # 16 Integer,the number of output filters in the convolution
    conv13= layers.Conv2D(16,(3,3),activation="relu",padding="same")(conv12)
    pool1 = layers.MaxPool2D((2,2))(conv13)
    drop1 = layers.Dropout(0.5)(pool1)
   #block2 64x64
    conv21 = layers.Conv2D(32,(3,3),activation="relu",padding="same")(drop1)
    conv22 = layers.Conv2D(32,(3,3),activation="relu",padding="same")(conv21)
    conv23 = layers.Conv2D(32,(3,3),activation="relu",padding="same")(conv22)
    pool2 = layers.MaxPool2D((2,2))(conv23)
    drop2 = layers.Dropout(0.5)(pool2)
    #block3 32x32
    conv31 = layers.Conv2D(64,(3,3),activation="relu",padding="same")(drop2)
    conv32 = layers.Conv2D(64,(3,3),activation="relu",padding="same")(conv31)
    conv33 = layers.Conv2D(64,(3,3),activation="relu",padding="same")(conv32)
    pool3 = layers.MaxPool2D((2,2))(conv33)
    drop3 = layers.Dropout(0.5)(pool3)

    #block4 16x16
    conv41 = layers.Conv2D(128,(3,3),activation="relu",padding="same")(drop3)
    conv42 = layers.Conv2D(128,(3,3),activation="relu",padding="same")(conv41)
    conv43 = layers.Conv2D(128,(3,3),activation="relu",padding="same")(conv42)
    pool4 = layers.MaxPool2D((2,2))(conv43)
    drop4 = layers.Dropout(0.5)(pool4)
    
    #bottom of Unet 8x8
    conv5 = layers.Conv2D(256,(3,3),activation="relu",padding="same")(drop4)
    conv5 = layers.Conv2D(256,(3,3),activation="relu",padding="same")(conv5)

    #upblock4 16x16
    x = layers.UpSampling2D((2,2))(conv5)
    x = layers.Conv2D(128,(3,3),activation="relu",padding="same")(x)
    x = layers.concatenate([conv43,x])
    x= layers.Conv2D(128,(3,3),activation="relu",padding="same")(x)
    x = layers.Conv2D(128,(3,3),activation="relu",padding="same")(x)
    x = layers.Dropout(0.5)(x)
    #upblock3 32x32
    x = layers.UpSampling2D((2,2))(x)
    x = layers.Conv2D(64,(3,3),activation="relu",padding="same")(x)
    x = layers.concatenate([conv33,x])
    x= layers.Conv2D(64,(3,3),activation="relu",padding="same")(x)
    x= layers.Conv2D(64,(3,3),activation="relu",padding="same")(x)
    x = layers.Dropout(0.5)(x)
    #upblock2 64x64
    x = layers.UpSampling2D((2,2))(x)
    x = layers.Conv2D(32,(3,3),activation="relu",padding="same")(x)
    x = layers.concatenate([conv23,x])
    x= layers.Conv2D(32,(3,3),activation="relu",padding="same")(x)
    x= layers.Conv2D(32,(3,3),activation="relu",padding="same")(x)
    x = layers.Dropout(0.5)(x)
    #upblock1 128x128
    x = layers.UpSampling2D((2,2))(x)
    x = layers.Conv2D(16,(3,3),activation="relu",padding="same")(x)
    x = layers.concatenate([conv13,x])
    x= layers.Conv2D(16,(3,3),activation="relu",padding="same")(x)
    x= layers.Conv2D(16,(3,3),activation="relu",padding="same")(x)
    x = layers.Dropout(0.5)(x)
    #to label image (2 labels)
    x = layers.Conv2D(labels,(1,1))(x)
    if out_activation == "sigmoid":
        outputs = layers.Activation("sigmoid")(x)
    elif out_activation == "softmax":
        outputs =MySoftmax()(x)
    elif  out_activation == None:
        outputs = x
    model = Model(inputs=inputs,outputs=outputs)
    return model
    
    
    
    
