#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015  Sergio Carlón Ruiz - All rights reserved
########################################################################
#                                                                      #
#  HackForGood2015	                                                   #
#                                                                      #
#  LORCA -no el pueblo, ni el poeta; sino el PROYECTO                  #
#                                                                      #
########################################################################

import os
import sys
import numpy as np
import cv2
import copy
from matplotlib import pyplot as plt
import time
import thread
webcam =0
quit_button= 'q'
LANGUAGE = "spa"
ocupado = True
mask = None

def syscall(command):
  f = os.popen(command)
  response = f.read()
  return response

def image_to_text(image):
  text_response = syscall("tesseract "+ image +" stdout -l "+LANGUAGE)
  clean_text = text_response.replace("\n", " ")
  return clean_text

def aplanador(text):
  text = text.replace("á","a")
  text = text.replace("é","e")
  text = text.replace("í","i")
  text = text.replace("ó","o")
  text = text.replace("ú","u")
  text = text.replace("Á","A")
  text = text.replace("É","E")
  text = text.replace("Í","I")
  text = text.replace("Ó","O")
  text = text.replace("Ú","u")
  text = text.replace("ñ","ni")
  text = text.replace("¿","")
  text = text.replace("?","")
  text = text.replace("!","")
  text = text.replace("¡","")
  text = text.replace(">","")
  text = text.replace("<","")
  text = text.replace("`","")
  text = text.replace("'","")
  text = text.replace("'","")
  return text
def use_festival(text):
  fich = file("leer","w")
  text=aplanador(text)
  print "A leer: "+text
  fich.write(text)
  fich.close()
  syscall("cat leer | festival --tts --language spanish")

def collect_words():
  global mask
  global ocupado

  while True:
    time.sleep(3)
    cv2.imwrite('img.png',mask)
    ocupado = True
    read_collected_word()
    ocupado = False

def read_collected_word ():
  text = image_to_text("img.png")
  use_festival(text)

def video_window():
  global ocupado
  global mask
  cap = cv2.VideoCapture(webcam)

  x=150
  y=200
  x1=350
  y1=75

  while(True):
    # Capture frame-by-frame
    zret, frame = cap.read()
    captura=frame.copy()
    #rectangulo
    if ocupado == True:
      cv2.rectangle(frame,(x,y),(x+x1,y+y1),(0,0,255),2)
    else:
      cv2.rectangle(frame,(x,y),(x+x1,y+y1),(0,255,0),2)
    #mascara
    captura=cv2.cvtColor(captura, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(captura.shape,np.uint8)
    mask[y:y+y1,x:x+x1] = captura[y:y+y1,x:x+x1]
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord(quit_button):
      break

thread.start_new_thread(collect_words, tuple())
video_window()
#text_to_read = image_to_text(sys.argv[1])
#use_festival(text_to_read)


