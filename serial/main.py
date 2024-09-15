import serial
ser = serial.Serial("COM11", 115200)

while True:
    cc=str(ser.readline())
    print(cc)