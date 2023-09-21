import serial
import time
import os
import random
import uuid
from ultralytics import YOLO
import cv2

def return_char(name):
    if name == 'RED':
        return 'w'
    if name == 'GREEN':
        return 'x'
    if name == 'BLUE':
        return 'y'
    if name == 'YELLOW':
        return 'z'
    if name == 'CODE1':
        return '1'
    if name == 'CODE2':
        return '2'
    if name == 'CODE3':
        return '3'
    if name == 'CODE4':
        return '4'
    if name == 'CODE5':
        return '5'
    if name == 'CODE6':
        return '6'
    if name == 'CODE7':
        return '7'
    if name == 'CODE8':
        return '8'
    if name == 'CODE9':
        return '9'
    if name == 'LETTERA':
        return 'a'
    if name == 'LETTERB':
        return 'b'
    if name == 'LETTERC':
        return 'c'
    if name == 'LETTERD':
        return 'd'
    if name == 'LETTERE':
        return 'e'
    if name == 'LETTERF':
        return 'f'
    if name == 'LETTERG':
        return 'g'
    if name == 'LETTERH':
        return 'h'
    if name == 'LETTERI':
        return 'i'
    
    
def predict_cube():
    cap = cv2.VideoCapture(0)
    model_path = 'best.pt'
    model = YOLO(model_path)  # load a custom model
    threshold = 0.5

    ret, frame = cap.read()

    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if score > threshold:
            name = model.names[int(class_id)].upper()
            cap.release()
            cv2.destroyAllWindows()
            return return_char(name)


# ser = serial.Serial("/dev/ttyACM0", 9600, timeout = 1)
# ser = serial.Serial("/dev/ttyACM0", 9600, timeout = 1)
ser = serial.Serial("COM8", 9600, timeout = 1)
# i = 0
# response = ser2.read()
# print(response.decode('utf-8'))

while True:
    try:
        data = ser.read()
        print(data.decode('utf-8'))
        if "p" in data.decode('utf-8'):
            char = predict_cube()
            for i in range(1000):
                ser.write(char.encode('utf-8'))

    except:
        pass
    # string = f"{i} Oi sdds\n"
    # ser.write(string.encode())
    # i+=1
    
    # response = ser2.read()
    # print(type(response))
    # print(response.decode('utf-8'))
    # print("Arduino respondeu: ", )
    # ser2.write("j".encode('utf-8'))
    # print("enviei")

ser.close()