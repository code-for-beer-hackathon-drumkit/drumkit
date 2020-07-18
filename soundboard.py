import pygame.mixer					#for the sound
import serial						#for serial input from the Arduino
import time						#for metronome
from sys import exit					#to quit on interrupt
import RPi.GPIO as GPIO					#makeshift switch on the Pi
import datetime						#for timestamp

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)					#change GPIO pings according to convenience on the Pi
GPIO.setup(26,GPIO.IN)

pygame.mixer.init(44100,-16,2,2048)			#Sound init, values taken from the sound samples we play
sndB=pygame.mixer.Sound("Crash-Cymbal-1.wav")		#Sound objects
sndA=pygame.mixer.Sound("bass.wav")
sndC=pygame.mixer.Sound("E-Mu-Proteus-FX-Wacky-Snare.wav")
sndD=pygame.mixer.Sound("metronome.wav")
sndE=pygame.mixer.Sound("track.wav")

sChA = pygame.mixer.Channel(1)				#Sound Channels
sChB = pygame.mixer.Channel(2)
sChC = pygame.mixer.Channel(3)
sChD = pygame.mixer.Channel(4)
sChE = pygame.mixer.Channel(5)

snr0=1000						#Values for thresholds and sensor separation
snr1=2000
snr2=3000
snr3=4000
calVal=15						#value for calibration purposes
mytime=time.time()					#For metronome frequencies
getTrack=0						#Keeps track of the music track playing

f = open("output.log","a")

ser = serial.Serial("/dev/ttyACM0", 9600)		#R-Pi to Arduino device

print("Sampler Ready")

while True:
	try:
		if(GPIO.input(23)==True):
			if(flag==0):		#toggle switches instead of a constant on or ff
				flag=1
			else:
				flag=0

			if (flag==1 and (time.time()-mytime >= 0.5)):		#play metronome sample at 0.5 seconds
				sChD.play(sndD)
				mytime=time.time()
				value = datetime.datetime.fromtimestamp(time.time())
				print(value.strftime('%Y-%m-%d %H:%M:%S'),"\tMetronome")
				f.write(value.strftime('%Y-%m-%d %H:%M:%S')+"\tMetronome\n")
				
		if(GPIO.input(26)==True):		#toggle switch works just as fine
			if(getTrack==0):
				print("GPIO 26 is now online")
				getTrack=1
				sChE.play(sndE)
				value = datetime.datetime.fromtimestamp(time.time())
				print(value.strftime('%Y-%m-%d %H:%M:%S'),"\tTrack")
				f.write(value.strftime('%Y-%m-%d %H:%M:%S')+"\tTrack\n")
				
			else
				getTrack=0
				sChE.stop()
				value = datetime.datetime.fromtimestamp(time.time())
				print(value.strftime('%Y-%m-%d %H:%M:%S'),"\tNo Track")
				f.write(value.strftime('%Y-%m-%d %H:%M:%S')+"\tNo Track\n")
		
		if(ser.in_waiting):
			myData = ser.readline()
			if (myData == b'\n'):		#this should no longer occur, but I'm not changing this without testing
                            continue
                            
			if(int(myData) < snr1 and int(myData) > 1000+calVal):
				sndA.set_volume((int(myData)-snr0)/snr0*10)
				sChA.play(sndA)
				value = datetime.datetime.fromtimestamp(time.time())
				print(value.strftime('%Y-%m-%d %H:%M:%S'),sndA.get_volume(),"\tDevice 1")
				f.write(value.strftime('%Y-%m-%d %H:%M:%S ')+str(sndA.get_volume())+"\tDevice 1\n")
				
			if(int(myData) < snr2 and int(myData) > snr1+calVal):
				sndB.set_volume((int(myData)-snr1)/snr0*10)
				sChB.play(sndB)
				value = datetime.datetime.fromtimestamp(time.time())
				print(value.strftime('%Y-%m-%d %H:%M:%S'),sndB.get_volume(),"\tdevice 2")
				f.write(value.strftime('%Y-%m-%d %H:%M:%S ')+str(sndB.get_volume())+"\tdevice 2\n")
				
			if(int(myData) < snr3 and int(myData) > snr2+calVal):
				sndC.set_volume((int(myData)-snr2)/snr0*10)
				sChC.play(sndC)
				value = datetime.datetime.fromtimestamp(time.time())
				print(value.strftime('%Y-%m-%d %H:%M:%S'),sndC.get_volume(),"\tDevice 3")
				f.write(value.strftime('%Y-%m-%d %H:%M:%S ')+str(sndC.get_volume())+"\tDevice 3\n")
		
			myData = b'0\n'		#Do we even need this ?
	except KeyboardInterrupt:
		exit()
