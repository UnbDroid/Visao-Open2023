import serial
import time
import os
import random
import uuid
from ultralytics import YOLO
import cv2

def random_hex_name():
    if not hasattr(random_hex_name, "first_call"):
        random_hex_name.first_call = int(uuid.uuid4().hex[:8], 16)
        random_hex_name.counter = 1
        return hex(random_hex_name.first_call)[2:]
    else:
        random_hex_name.counter += 1
        return hex(random_hex_name.first_call + random_hex_name.counter)[2:]


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
    else:
        return '0'
    
def predict_cube(cap, model):

    threshold = 0.5

    ret, frame = cap.read()

    original_frame = frame.copy()

    good_results = {}

    results = model(frame)[0]
    name = None
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if score > threshold:
            name = model.names[int(class_id)].upper()
            if x1 > 50 and x2 < 550:
                good_results[name] = y2
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, "{} {:.2f}".format(name, score), (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
        
    if good_results:
        name = max(good_results, key=good_results.get)
    cv2.putText(frame, f"Eu vejo {name}", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 0), 3, cv2.LINE_AA)
    # cv2.imshow("foto", frame)
    random_name = random_hex_name()
    save_path = os.path.join("..","images_predict", f"{random_name}.png")
    cv2.imwrite(save_path, frame)
    save_path = os.path.join("..","images_no_predict", f"{random_name}.png")
    cv2.imwrite(save_path, original_frame)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return return_char(name)

def count_cubes(cap, model):

    threshold = 0.5

    ret, frame = cap.read()

    original_frame = frame.copy()

    good_results = 0

    results = model(frame)[0]
    name = None
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if score > threshold:
            name = model.names[int(class_id)].upper()
            if y2 > 300:
                good_results += 1
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, "{} {:.2f}".format(name, score), (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
        
    
    if good_results > 9:
        good_results = 9
    
    cv2.putText(frame, f"Eu vejo {good_results} cubos", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 0), 3, cv2.LINE_AA)
    # cv2.imshow("foto", frame)
    random_name = random_hex_name()
    save_path = os.path.join("..","images_predict", f"{random_name}.png")
    cv2.imwrite(save_path, frame)
    save_path = os.path.join("..","images_no_predict", f"{random_name}.png")
    cv2.imwrite(save_path, original_frame)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return(str(good_results))


def do_action(cap, model_cubes, ser):
    data = ser.read()
    if "t" in data.decode('utf-8'):
        print("entrei")
        c = predict_cube(cap, model_cubes)
        print(c)    
        for i in range(1000):
            ser.write(c.encode('utf-8'))
    
    elif "p" in data.decode('utf-8'):
        pass

    elif "k" in data.decode('utf-8'):
        print("entrei contando")
        c = count_cubes(cap, model_cubes)
        print(c)
        for i in range(1000):
            ser.write(c.encode('utf-8'))
        

i = 0
for i in range(10):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        break

model_cubes = YOLO('/home/droid/Documentos/Visao-Open2023/cubes2.pt')
print('sai')

ports_list = ['ACM0', 'ACM1', 'ACM2', 'USB0', 'USB1']
while True:
    for port in ports_list:
        try:
            ser = serial.Serial("/dev/tty" + port, 9600, timeout = 1)
            while True:
                do_action(cap, model_cubes, ser)
                print('sai')
        except:
            pass

   