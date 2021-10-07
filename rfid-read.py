import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests
import time
import os
import csv
from datetime import datetime
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
red = 37
green = 36
GPIO.setup(green, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)

#get data from rfid as well as serial number
# change "name" variable to "info" and accept relevant info
#instead of name of tag holder

reader= SimpleMFRC522()

def read_card():
    card_d = None
    card_id, data = reader.read()
    now = datetime.now()
    return card_id, now, data

values = []
def store_values(value, DT, data):
    DT_string = DT.strftime("%d/%m/%Y %H:%M:%S")
    values.append([value, DT_string, data])
    write_csv(values) #forward values found to write_csv. 

def write_csv(values):
    f = open('datafile.csv', 'w', newline = "") #open csv file named datafile and write each new line inside ""
    pen = csv.writer(f) #pen will help in writing data in files, initalising pen
    pen.writerow(["Serial Number", "DateTime", "Information"]) #writing headers for each column
    for events in values: # events is a sublist in values
        pen.writerow([str(events)[1:51]]) #writing sublist events as a string value in each row, removing brackets [] of each sublist by slicing
    f.close() #closing file 
    

      
def green_led():
    GPIO.output(green, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(green, GPIO.LOW)
    
def red_led():
    GPIO.output(red, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(red, GPIO.LOW)

def data_check():
    card_id, DT, data = read_card()
    if card_id != None and data[0:4] == "1234":
        print(card_id)
        store_values(card_id, DT, data)
        green_led()
     
    else:
        print("Data not read properly, entry not stored in file")
        red_led()
        
    print(data[0:4])
    print(values)
    main()

def main():
    try:
        print("running....")
        data_check()
        
    except KeyboardInterrupt:
        print("Quit")
        GPIO.cleanup()
  
main()

 