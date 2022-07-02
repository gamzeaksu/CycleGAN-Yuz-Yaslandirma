# -- coding: utf-8 --
"""
Created on Wed May 18 23:26:08 2022

@author: CASPER
"""

from tkinter import *
import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk
import PIL
import tkinter
import tkinter.filedialog
from io import BytesIO
import  os
from keras.models import load_model
from keras_contrib.layers.normalization.instancenormalization import InstanceNormalization
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

class faceaging:
    myimage = None
    filename = 'path'
    selilen = None
    secimg = None
    def main(self,f):
        f.title('Yüz Yaşlandırma')
        f.geometry('700x1000')
        f["background"]="#FFCCCC"
        #f.resizable(width =False, height=False)
        
        title = Label(f,text='Yüz Yaşlandırma')
        title.config(font=('Comic Sans MS', 33),bg="#FFCCCC")
        #title.grid(, anchor=CENTER)
        title.place(relx=0.5, rely=0.02, anchor=N)
        load = Image.open("young-and-old-woman-face-aging-concept-isolated-vector-21030727.jpg")

        resize_image = load.resize((290, 300))
         
        img = ImageTk.PhotoImage(resize_image)
 
        panel = Label(f, image=img,bg='#FF9999')
        panel.image = img
        panel.place(relx=0.5, rely=0.12, anchor=N)
        b_yukle = Button(f,text="Yükle",command= lambda : self.yukle(f), padx=14)
        b_yukle.config(font=('Comic Sans MS',14),
                       bg="#FF9999")
        b_yukle.place(relx=0.35, rely=0.45, anchor=N)

        b_yaslandir = Button(f, text="Yaşlandır",padx=14,command=lambda :self.yaslandir(f,self.myimage))
        b_yaslandir.config(font=('Comic Sans MS',14),
                       bg="#FF9999")
        b_yaslandir.place(relx=0.63, rely=0.45, anchor=N)
        
    def normalization(self, images):
        images = (images - 127.5) / 127.5
        return images
    def preprocess(self,path):
        images_A = []
        for filepath in path:
            img = np.array(Image.open(filepath).convert('RGB').resize((128, 128)))
            images_A.append(img)
        images_A = np.array(images_A)
    def yukle(self,f):
        myfile = tkinter.filedialog.askopenfilename(filetypes = ([('jpg', '.jpg'), ('All Files', '.*')]))
        print(myfile)
        if not myfile:
            messagebox.showerror("Error","Görüntü seçmediniz!")
        else:
            myimg = Image.open(myfile, 'r')
            l = []
            img = np.array(myimg.resize( (128,128),Image.ANTIALIAS))
            l.append(img)
            l = np.array(l)
            img = l
            if img is not None:
                img = self.normalization(img)
                print(img.shape)
            x_out = generator_AtoB.predict(img)
            #rescale
            x_out = (x_out + 1) / 2.0
            print(x_out[0].shape)
            #fig = plt.figure(figsize=(4, 4))
            #plt.imshow(x_out)
            x_out = x_out[0]*255
            print(x_out)
            img = Image.fromarray(np.uint8(x_out)).convert('RGB')
            self.myimage = img
            """
            print(type(x_out))
            #fig = plt.figure(figsize=(4, 4))
            plt.imshow(x_out)
            plt.imsave('Fakes\\1-.jpg', x_out)
            img = Image.fromarray(x_out,'RGB')
            print(img.shape)
            img.save('Fakes\\1.jpg')
            img = Image.fromarray(x_out,'RGBA')
            #print(img.shape)
            img.save('Fakes\\1.jpg')"""
            
            myimage = myimg.resize((300, 300))

            img = ImageTk.PhotoImage(myimage)
            #print("f1:",self.myimage.filename)
            l4= Label(f,text='Seçilen Görüntü:')
            l4.config(font=('Comic Sans MS',18),
                       bg="#FFCCCC")
            l4.place(relx=0.25, rely=0.53, anchor=N)
            self.secilen = l4
            panel = Label(f, image=img, bg='#FF9999')
            panel.image = img
            panel.place(relx=0.25, rely=0.59, anchor=N)
            self.secimg = panel
            
    def clear(self,panel,label):
        panel.config(image='',
                     bg = '#FFCCCC')
        self.secimg.config(image='',
                           bg = '#FFCCCC')
        label.config(text='')
        self.secilen.config(text='')
    def yaslandir(self, f, myimg):
        newimg = myimg
        #newimg = Image.open(newimg)
        my_file = BytesIO()
        newimg = newimg.resize((300, 300))
        img = ImageTk.PhotoImage(newimg)
        #print("f1:",self.myimage.filename)
        l4= Label(f,text='Yaşlanmış Görüntü:')
        l4.config(font=('Comic Sans MS',18),
                   bg="#FFCCCC")
        l4.place(relx=0.75, rely=0.53, anchor=N)
        panel = Label(f, image=img, bg='#FF9999')
        panel.image = img
        panel.place(relx=0.75, rely=0.59, anchor=N)
        
        b_back = Button(f, text="Yeniden",padx=14,command=lambda :self.clear(panel,l4))
        b_back.config(font=('Comic Sans MS',14),
                       bg="#FF9999")
        #b_back.visible = False
        b_back.place(relx=0.5, rely=0.93, anchor=N)


cust = {'InstanceNormalization': InstanceNormalization, 'tf': tf}
generator_AtoB =  load_model('C:/Users/cansu/Desktop/bitirme_proje/UTK/Generated/g_model_AtoB_049000.h5',cust, compile=False)
      
f = Tk()  
face = faceaging()
face.main(f)
f.mainloop()