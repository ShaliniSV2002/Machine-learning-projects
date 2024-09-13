import numpy as np
import cv2
import random
from gtts import gTTS
import os
# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
import smbus
from time import sleep
from email import encoders #The email package provides some convenient encoders in its encoders module. 
from time import sleep #Python has a module named time which provides several useful functions to handle time-related tasks.
from email.mime.multipart import MIMEMultipart# MIMEMultipart is for saying "I have more than one part", and then listing the parts - you do that if you have attachments
from email.mime.base import MIMEBase# MIMEBase is provided primarily as a convenient base class for more specific MIME-aware subclasses.(text or image)  
from email.mime.text import MIMEText # MimeText is used for sending text emails.
from email.utils import formatdate# for date
from datetime import datetime# packageto get actual date and time
fromaddr = "sender@gmail.com" # sender mail adress

#toaddr = "surajajjampur@gmail.com"
toaddr = "receiver@gmail.com" #receiver mail address

msg = MIMEMultipart()# making message as multi part

msg['From'] = fromaddr

msg['To'] = toaddr

msg['Subject'] = "SUBJECT OF THE EMAIL"

body = "check attached file"
# Print a two line message

class MLX90614():

    MLX90614_RAWIR1=0x04
    MLX90614_RAWIR2=0x05
    MLX90614_TA=0x06
    MLX90614_TOBJ1=0x07
    MLX90614_TOBJ2=0x08

    MLX90614_TOMAX=0x20
    MLX90614_TOMIN=0x21
    MLX90614_PWMCTRL=0x22
    MLX90614_TARANGE=0x23
    MLX90614_EMISS=0x24
    MLX90614_CONFIG=0x25
    MLX90614_ADDR=0x0E
    MLX90614_ID1=0x3C
    MLX90614_ID2=0x3D
    MLX90614_ID3=0x3E
    MLX90614_ID4=0x3F

    comm_retries = 5
    comm_sleep_amount = 0.1

    def __init__(self, address=0x5a, bus_num=1):
        self.bus_num = bus_num
        self.address = address
        self.bus = smbus.SMBus(bus=bus_num)

    def read_reg(self, reg_addr):
        err = None
        for i in range(self.comm_retries):
            try:
                return self.bus.read_word_data(self.address, reg_addr)
            except IOError as e:
                err = e
                #"Rate limiting" - sleeping to prevent problems with sensor
                #when requesting data too quickly
                sleep(self.comm_sleep_amount)
        #By this time, we made a couple requests and the sensor didn't respond
        #(judging by the fact we haven't returned from this function yet)
        #So let's just re-raise the last IOError we got
        raise err

    def data_to_temp(self, data):
        temp = (data*0.02) - 273.15
        return temp

    def get_amb_temp(self):
        data = self.read_reg(self.MLX90614_TA)
        return self.data_to_temp(data)

    def get_obj_temp(self):
        data = self.read_reg(self.MLX90614_TOBJ1)
        return self.data_to_temp(data)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
upper_body = cv2.CascadeClassifier('haarcascade_upperbody.xml')
nose_cascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')

if nose_cascade.empty():
  raise IOError('Unable to load the nose cascade classifier xml file')


# Adjust threshold value in range 80 to 105 based on your light.
bw_threshold = 80

# User message
font = cv2.FONT_HERSHEY_SIMPLEX
org = (30, 30)
weared_mask_font_color = (36, 255, 25)
not_weared_mask_font_color = (0, 0, 255)
thickness = 2
font_scale = 1
weared_mask = "THANK YOU FOR WEARING MASK"
not_weared_mask = "ALERT!! WEAR MASK DEFEAT CORONA"

# Read video
cap = cv2.VideoCapture(0)

while 1:
    # Get individual frame
    sensor = MLX90614()
    #print(sensor.get_amb_temp())
    #print('Temperature=')
    tempe = sensor.get_obj_temp()
    print('Temperature=',sensor.get_obj_temp())
    if tempe>36:
        text = 'Temperature is'+str(tempe)
        print(text)
        print("Converting your text to sound . . .")
        tts = gTTS(text="how are you", lang='en')
        tts.save("voice.mp3")
        print("Starting audio. . .")
        sleep(2)
        text = 'Temperature high stop'
        print(text)
        print("Converting your text to sound . . .")
        tts = gTTS(text="how are you", lang='en')
        tts.save("voice.mp3")
        print("Starting audio. . .")
        sleep(2)
    if tempe<36:
        text = 'Temperature is'+str(tempe)
        print(text)
        print("Converting your text to sound . . .")
        tts = gTTS(text="how are you", lang='en')
        tts.save("voice.mp3")
        print("Starting audio. . .")
        sleep(2)
        text = 'Temperature low you are good to go'
        print(text)
        print("Converting your text to sound . . .")
        tts = gTTS(text="how are you", lang='en')
        tts.save("voice.mp3")
        print("Starting audio. . .")
        sleep(2)
    ret, img = cap.read()
    img = cv2.flip(img,1)

    # Convert Image into gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Convert image in black and white
    (thresh, black_and_white) = cv2.threshold(gray, bw_threshold, 255, cv2.THRESH_BINARY)
    #cv2.imshow('black_and_white', black_and_white)

    # detect face
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Face prediction for black and white
    faces_bw = face_cascade.detectMultiScale(black_and_white, 1.1, 4)


    if(len(faces) == 0 and len(faces_bw) == 0):
        cv2.putText(img, "FACE NOT FOUND....", org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
        msg.attach(MIMEText(body, 'plain'))# for attaching mail with body as plain text
                part = MIMEBase('application', 'octet-stream')# convert the email data octet stream for supporting to gmail

                part.set_payload((attachment).read())

                encoders.encode_base64(part)# encode as per gmail

                part.add_header('Content-Disposition', "attachment; filename= %s" % filename)# add headers

                msg.attach(part)# attach 

                server = smtplib.SMTP('smtp.gmail.com', 587)# open gmail through port 587

                server.starttls()# start the gmail server

                server.login(fromaddr, "password")# loging to gmail with user id and password

                text = msg.as_string()# conver whole message as string

                server.sendmail(fromaddr, toaddr, text)# send mail

                server.quit()# quit gmail server
    elif(len(faces) == 0 and len(faces_bw) == 1):
        # It has been observed that for white mask covering mouth, with gray image face prediction is not happening
        cv2.putText(img, weared_mask, org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
    else:
        # Draw rectangle on gace
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]


            # Detect lips counters
            mouth_rects = mouth_cascade.detectMultiScale(gray, 1.5, 5)
            nose_rects = nose_cascade.detectMultiScale(gray, 1.3, 5)
        # Face detected but Lips not detected which means person is wearing mask
        if((len(mouth_rects) == 0) and (len(nose_rects) == 0)):
            cv2.putText(img, weared_mask, org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
        else:
            #for (mx, my, mw, mh) in mouth_rects:

                #if(y < my < y + h):
                    # Face and Lips are detected but lips coordinates are within face cordinates which `means lips prediction is true and
                    # person is not waring mask
                    cv2.putText(img, not_weared_mask, org, font, font_scale, not_weared_mask_font_color, thickness, cv2.LINE_AA)
                    door=1;
                    sleep(3);
                    door=0;
                    
                    #cv2.rectangle(img, (mx, my), (mx + mh, my + mw), (0, 0, 255), 3)
                    #break

    # Show frame with results
    cv2.imshow('Mask Detection', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# Release video
cap.release()
cv2.destroyAllWindows()
