import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests
import time
import os
#import sqlite3 # Install mysql-connector-python BELOW!!
import mysql.connector
# pip install mysql-connector-python
from datetime import datetime
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
red = 37
green = 36
GPIO.setup(green, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)
# Changing the connection from local sqlite3 database
# connection = sqlite3.connect('datalogger.db')
connection = mysql.connector.connect(host='rfidcheckin.cljhbnnuplh1.ap-southeast-2.rds.amazonaws.com',database='rfidDB',user='admin',password='PASSWORD HERE')

cursor = connection.cursor()

#get data from rfid as well as serial number
# change "name" variable to "info" and accept relevant info
#instead of name of tag holder
class Logger:
    def __init__(self):
        self.values = []
        #self.card_ID = card_ID
        #self.now = now
        #self.data = data
        self.reader= SimpleMFRC522()

    def read_card(self):
        card_id = None
        card_id, data = self.reader.read()
        now = datetime.now()
        latest_entry = (card_id, now, data)
        self.values.append(latest_entry)
        #return card_id, now, data
            
    def store_data(self):
        #print(self.data_dict)
        #for table, data in self.data_dict.items():
            #print(data)
        #values = (self.card_ID, self.now, self.data)
        #print(values)
        #cnt = len(data)-1
            #params = '?' + ',?'*cnt
        latest_row = self.values[-1]
        card_id = latest_row[0]
        date_time = latest_row[1]
        tag_info = latest_row[2]
        
        values_to_insert = (card_id, date_time, tag_info)
        
       # sql = "INSERT INTO Tag (Tag_ID_number, Time_recorded, Information) VALUES (%s, %s, %s)"
        #sql = "INSERT INTO Tag (Tag_ID_number, Time_recorded, Information) VALUES ('12345678', '20120618 10:34:09 AM', '1234Test_Data')" 
       # cursor.execute(sql, values_to_insert)
        cursor.execute("INSERT INTO rfidDB.Tag (Tag_ID, Time_recorded, Information) VALUES ('12345678', '2020-12-22 06:49:46', '1234Test_Data')")
        connection.commit()
        
        print(cursor.rowcount, "record inserted")
        
            
          
    def green_led(self):
        GPIO.output(green, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(green, GPIO.LOW)
        
    def red_led(self):
        GPIO.output(red, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(red, GPIO.LOW)

    def data_check(self):
        
       # last_entry = list(self.data_dict.keys())[-1]
        latest_row = self.values[-1]
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
        cursor.close()
        connection.close()

        GPIO.cleanup()
  
main()

 
