
import smbus			#import SMBus module of I2C
from time import sleep          #import
from gtts import gTTS 
import pygame 
import os 
import RPi.GPIO as GPIO
import random
import sys
import iothub_service_client
from iothub_service_client import IoTHubMessaging, IoTHubMessage, IoTHubError



OPEN_CONTEXT = 0
FEEDBACK_CONTEXT = 1
MESSAGE_COUNT = 1
AVG_WIND_SPEED = 10.0
MSG_TXT = " ALERT!!!!!!!!!!! EARTHQUAKE AT IIT JODHPUR ,KARWAR ,JODHPUR , DESTRUCTION LEVEL : 56% , EARTHQUAKE READING : "




CONNECTION_STRING = "HostName=EarthquakeDetector.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=SgynxjuAKmXp/Jm4wZxQNpyfcTuA0GaFPZUe+r12p48="
DEVICE_ID = "pi"

def open_complete_callback(context):
    print ( 'open_complete_callback called with context: {0}'.format(context) )

def send_complete_callback(context, messaging_result):
    context = 0
    print ( 'send_complete_callback called with context : {0}'.format(context) )
    print ( 'messagingResult : {0}'.format(messaging_result) )



GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)


MotorA=16
Motor1B=22
Motor1E=22

GPIO.setup(MOTOR1A,GPIO.OUT)
GPIO.setup(MOTOR1B,GPIO.OUT)
GPIO.setup(MOTOR1E,GPIO.OUT)

  
#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47




def iothub_messaging_sample_run(final):
    try:
        iothub_messaging = IoTHubMessaging(CONNECTION_STRING)

        iothub_messaging.open(open_complete_callback, OPEN_CONTEXT)

        for i in range(0, MESSAGE_COUNT):
            print ( 'Sending message: {0}'.format(i) )
	    
            msg_txt_formatted = MSG_TXT + str(final)
            message = IoTHubMessage(bytearray(msg_txt_formatted, 'utf8'))

            # optional: assign ids
            message.message_id = "message_%d" % i
            message.correlation_id = "correlation_%d" % i
            # optional: assign properties
            prop_map = message.properties()
            prop_text = "PropMsg_%d" % i
            prop_map.add("Property", prop_text)

            iothub_messaging.send_async(DEVICE_ID, message, send_complete_callback, i)

        try:
            # Try Python 2.xx first
            raw_input("Press Enter to continue...\n")
        except:
            pass
            # Use Python 3.xx in the case of exception
            input("Press Enter to continue...\n")

        iothub_messaging.close()
	music()

    except IoTHubError as iothub_error:
        print ( "Unexpected error {0}" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubMessaging sample stopped" )
		


def save(final): 
	pygame.init()
	pygame.mixer.music.load("welcome.mp3")
	pygame.mixer.music.play()
	pygame.mixer.music.set_volume(100)
	GPIO.output(11,GPIO.HIGH)
	print("save yourself")
	print ( "Starting the IoT Hub Service Client Messaging Python sample..." )
    	print ( "    Connection string = {0}".format(CONNECTION_STRING) )
    	print ( "    Device ID         = {0}".format(DEVICE_ID) )
    
	print("going forward")

	GPIO.output(MOTOR1A,GPIO.HIGH)
	GPIO.output(MOTOR1B,GPIO.HIGH)
	GPIO.output(MOTOR1E,GPIO.HIGH)



    iothub_messaging_sample_run(final)

	sleep(10)
	
	GPIO.output(MOTOR1A,GPIO.LOW)
	GPIO.output(MOTOR1B,GPIO.LOW)
	GPIO.output(MOTOR1E,GPIO.LOW)

	GPIO.cleanup()


	exit()



def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)
	
def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    	
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value


bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

print (" Reading Data of Gyroscope and Accelerometer")

while True:
	
	
	#Read Gyroscope raw value
	gyro_x = read_raw_data(GYRO_XOUT_H)
	gyro_y = read_raw_data(GYRO_YOUT_H)
	gyro_z = read_raw_data(GYRO_ZOUT_H)
	
	Gx = gyro_x/131.0
	Gy = gyro_y/131.0
	Gz = gyro_z/131.0

	
	gyro_x2 = read_raw_data(GYRO_XOUT_H)
	gyro_y2 = read_raw_data(GYRO_YOUT_H)
	gyro_z2 = read_raw_data(GYRO_ZOUT_H)

	Gx2 = gyro_x2/131.0
	Gy2 = gyro_y2/131.0
	Gz2 = gyro_z2/131.0

	gyro_x1 = read_raw_data(GYRO_XOUT_H)
	gyro_y1 = read_raw_data(GYRO_YOUT_H)
	gyro_z1 = read_raw_data(GYRO_ZOUT_H)

	Gx1 = gyro_x1/131.0
	Gy1 = gyro_y1/131.0
	Gz1 = gyro_z1/131.0


	gyro_x3 = read_raw_data(GYRO_XOUT_H)
	gyro_y3 = read_raw_data(GYRO_YOUT_H)
	gyro_z3 = read_raw_data(GYRO_ZOUT_H)
	Gx3 = gyro_x3/131.0
	Gy3 = gyro_y3/131.0
	Gz3 = gyro_z3/131.0

	gyro_x4 = read_raw_data(GYRO_XOUT_H)
	gyro_y4 = read_raw_data(GYRO_YOUT_H)
	gyro_z4 = read_raw_data(GYRO_ZOUT_H)
	Gx4 = gyro_x4/131.0
	Gy4 = gyro_y4/131.0
	Gz4 = gyro_z4/131.0

	gyro_x5 = read_raw_data(GYRO_XOUT_H)
	gyro_y5 = read_raw_data(GYRO_YOUT_H)
	gyro_z5 = read_raw_data(GYRO_ZOUT_H)

	Gx5 = gyro_x5/131.0
	Gy5 = gyro_y5/131.0
	Gz5 = gyro_z5/131.0



	final=abs((Gx+Gx2+Gx1+Gx3+Gx4+Gx5)+abs(Gy+Gy2+Gy1+Gy3+Gy4+Gy5)+abs(Gz+Gz2+Gz1+Gz3+Gz4+Gz5))/10

	print(final)
	if final>0.50:
		save(final)

	'''
	Full scale range +/- 250 degree/C as per sensitivity scale factor
	Ax = acc_x/16384.0
	Ay = acc_y/16384.0
	Az = acc_z/16384.0
	'''
	#print("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az) 	
	sleep(1)
 
