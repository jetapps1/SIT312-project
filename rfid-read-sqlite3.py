import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests
import time
import os
import sqlite3
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
class Logger:
    def __init__(self):
        self.data_dict = {}
        self.reader= SimpleMFRC522()

    def read_card(self):
        card_id = None
        card_id, data = self.reader.read()
        now = datetime.now()
        self.data_dict['Tag_info'] = (card_id, now, data)
        return card_id, now, data
            
    def store_data(self):
        connection = sqlite3.connect('datalogger.db')
        cursor = connection.cursor()
        print(self.data_dict)
        for table, data in self.data_dict.items():
            cnt = len(data)-1
            params = '?' + ',?'*cnt
            cursor.execute(f"INSERT INTO {table} VALUES({params})", data)
            connection.commit()
        cursor.close()
        
            
          
    def green_led(self):
        GPIO.output(green, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(green, GPIO.LOW)
        
    def red_led(self):
        GPIO.output(red, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(red, GPIO.LOW)

    def data_check(self):
        
        last_entry = list(self.data_dict.keys())[-1]
        latest_row = self.data_dict[last_entry]
        card_id = latest_row[0]
        date_time = latest_row[1]
        tag_info = latest_row[2]
        print(tag_info[0:4])
        print(latest_row)
        
            
        if card_id != None and tag_info[0:4] == "1234":
            print(card_id)
            return True
        else:
            print("Data not read properly, entry not stored in file")
                
        return False
        


def main():
    try:
        logger = Logger()
        print("running....")
        while True:

            logger.read_card()
            if logger.data_check() == True:
                logger.store_data()
                logger.green_led()
            else:
                logger.red_led()
                continue
                 
    except KeyboardInterrupt:
        print("Quit")
        GPIO.cleanup()
  
main()

 