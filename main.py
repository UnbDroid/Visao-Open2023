import serial
import time

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
            break
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