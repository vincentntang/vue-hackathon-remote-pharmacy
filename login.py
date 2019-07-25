from tkinter import *
import tkinter.messagebox
from PIL import ImageTk,Image  
import cv2
import numpy as np
import os
import face_recognition
from tkinter import messagebox
import time
import pyzbar.pyzbar as pyzbar
import json
import serial
import requests
import pymongo
from pymongo import MongoClient

total = 1
dataset_img = os.listdir('dataset')
ser = serial.Serial('COM21' , 9600, timeout= 10)

#---------------------Scanning------------------------------------#

def face_scan():
    
    dataset_img = os.listdir('dataset')
    cap = cv2.VideoCapture(0)
    total = 0

    top = Toplevel()
    top.title('Scan')
    Message(top, text="Scan QR Code", padx=20, pady=20).place(x = 250 , y = 250)
    top.after(2000, top.destroy)
    stop = 0
    while True:
        _, frame = cap.read()
        cv2.imshow("Scan QR Code", frame)

        decodedObjects = pyzbar.decode(frame)
        for obj in decodedObjects:
            raw_data = (obj.data.decode())
            json_data = json.loads(raw_data)
            #print(json_data["patientID"])
            patient_id = json_data["patientID"]
            medi_name = json_data["medicationName"]
            medi_dose = json_data["dosage"]
            stop = 1
            break

        if cv2.waitKey(1) & stop == 1:
            break

    cv2.destroyAllWindows()
    cap.release()

    cluster = MongoClient("PUT MONGO STRING URI HERE")
    db = cluster["remotepharmacy"]
    collections = db["patients"]

    results = collections.find({"patientID":str(patient_id)})

    for result in results:
        url = (result["image"])
        name = result["patientname"]

    r = requests.get(url, allow_redirects=True)
    open('dataset/'+str(name)+'.jpg', 'wb').write(r.content)

    cap = cv2.VideoCapture(0)
    while True:
        _,frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
        total += 1

        cv2.imshow("Scan Face",frame)

        cv2.waitKey(1)
        if total == 5:
            #cv2.imwrite("test.jpg",frame[y1-20:y2+30,x1-20:x2+30])
            cv2.imwrite("test.jpg",frame)
            
            break
    
    new_image = face_recognition.load_image_file('test.jpg')
    new_image_encoded = face_recognition.face_encodings(new_image)[0]

    for image in dataset_img:
        current_img = face_recognition.load_image_file("dataset/" + image)
        current_img_encoded = face_recognition.face_encodings(current_img)[0]
        result = face_recognition.compare_faces([new_image_encoded],current_img_encoded)

    
        if result[0] == True:
            base = os.path.basename('dataset/'+image)
            person_id = os.path.splitext(base)[0]
            print ("matched: " + person_id)
            messagebox.showinfo("Login Success" , "Welcome "+str(person_id)+"")

            messagebox.showinfo("Medication" , "Name : "+str(medi_name)+"  Dosage : "+str(medi_dose)+"\n"+" Press Ok to Despense" )
            ser.write('b'.encode())
            dose_done()
            break
        else:
            messagebox.showinfo("Login Failed", "Patient Not Registered")
        break

    cv2.destroyAllWindows()
    cap.release()

#-----------------------Miss-------------------------------------#
def miss_route():

    url = "http://853f7148.ngrok.io/dispenseno"
    payload = ""
    headers = {
        'cache-control': "no-cache",
        'Postman-Token': "ad6714a9-5758-47aa-9a85-bc28a451d717"
        }
    response = requests.request("GET", url, data=payload, headers=headers)
    print(response.text)

#----------------------Done dose -------------------------------#
def dose_done():
    url = "http://853f7148.ngrok.io/dispenseyes"
    payload = ""
    headers = {
        'cache-control': "no-cache",
        'Postman-Token': "ad6714a9-5758-47aa-9a85-bc28a451d717"
        }
    response = requests.request("GET", url, data=payload, headers=headers)
    print(response.text)
#---------------------Home Page ---------------------------------#
root = Tk()
root.geometry("1920x1080")
root.title("Health Hacks")

frame = Frame(root, bg='#80c1ff')
#frame = Frame(root, highlightbackground="green", highlightcolor="green", highlightthickness=1, width=100, height=100, bd= 0)

frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.9)
load = Image.open("pill.png")
render = ImageTk.PhotoImage(load)
img = Label(frame, image=render)
img.image = render
img.place(x=800, y=300)
 

button_login = Button(frame, text="SCAN",command=face_scan)
#Lable_name = Label(frame, text="Remote Pharmacy")
button_miss = Button(frame, text="Miss",command=miss_route)

button_login.place(x=650,y=700, relheight=0.05, relwidth=0.3)
button_miss.place(x=800,y=780, relheight=0.05, relwidth=0.15)



root.mainloop()