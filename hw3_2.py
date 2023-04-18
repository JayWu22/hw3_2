import serial
import numpy as np
import time
import binascii
import struct

serdev = 'COM5'
ser = serial.Serial(serdev)

# define the textLCD commands
LOCATE = np.uint8([0x01])
CLS = np.uint8([0x02])
ROWS = np.uint8([0x03])
COLUMNS = np.uint8([0x04])
PUTC = np.uint8([0x05])


# send a command to the mbed program
def send_command(command, data):
    x = np.uint8(command)
    output = x.tobytes()
    ser.write(output)
    x = np.uint8(data)
    output = x.tobytes()
    ser.write(output)
    
while True:
    command = input("Enter a command (LOCATE, CLS, ROWS, COLUMNS, PUTC, or QUIT): ").upper()
    if command == "QUIT":
        break
    elif command == "LOCATE":
        row = int(input("Enter the row (0 or 1): "))
        column = int(input("Enter the column (0-15): "))
        data = np.uint8(row*16 + column)
        send_command(LOCATE, data)
    elif command == "CLS":
        send_command(CLS, 0X00)
    elif command == "ROWS":
        send_command(ROWS, 0X00)
        time.sleep(1)
        row = ser.read(1)
        row = int.from_bytes(row, 'little')
        print(row)
    elif command == "COLUMNS":
        send_command(COLUMNS, 0X00)
        time.sleep(1)
        column = ser.read(1)
        print(column)
        column = int.from_bytes(column, 'little')
        print(column)
    elif command == "PUTC":
        char = input("Enter the character: ")
        send_command(PUTC, np.uint8(ord(char)))
    else:
        print("Invalid command")

ser.close()
