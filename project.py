from time import sleep, strftime
from subprocess import *
import LCD_i2c.lcd_driver as lcd_driver
import serial
import MySQLdb
import thingspeak
import time

channel_id = 1557032
key = '08UF5J28KAE4SOCG'


lcd = lcd_driver.lcd()
lcd.lcd_clear()
ser = serial.Serial('/dev/ttyACM0',9600,timeout=1)
sleep(2)

channel = thingspeak.Channel(id=channel_id, api_key=key)

def thingspeak(channel):
    try:
        tem, hum = float(temperature), float(humidity)
        response = channel.update({'field1':tem, 'field2':hum})
    except:
        print("Connection fail")
        


while True:
        if ser.in_waiting > 0:
            rawserial = ser.readline()
            cookedserial = rawserial.decode('utf-8').strip('\r\n')
            datasplit = cookedserial.split(',')
            temperature = datasplit[0].strip('<')
            humidity = datasplit[1]
            distance = datasplit[2].strip('>')
            dbConn = MySQLdb.connect("localhost", "pi", "admin", "Project") or  die("Could not connect to the database")

            with dbConn:
                cursor = dbConn.cursor()
                cursor.execute("INSERT INTO Watering (Temperature, Humidity) values ({}, {})" .format( (float(temperature)), float(humidity)))
                dbConn.commit()
                cursor.close()
            
            print(temperature)
            print(humidity)
            if int(distance) < 100:
                line1 = "Temp(C): " +str(temperature)
                line2 = "Hum(%): " + str(humidity)
                lcd.lcd_display_string(line1, 1)
                lcd.lcd_display_string(line2, 2)
            else:
                lcd.lcd_clear()
                
            thingspeak(channel)
            
