#!/usr/bin/env python

import os
import glob
import time
import traceback
from time import sleep
import RPi.GPIO as GPIO
import picamera # http://picamera.readthedocs.org/en/release-1.4/install2.html
import atexit
import sys
import socket
import pygame
#import pytumblr # https://github.com/tumblr/pytumblr
import config
from signal import alarm, signal, SIGALRM, SIGKILL
import subprocess

import numpy as np
########################
### Variables Config ###
########################
button1_pin = 37 # pin for the big red button
flash_pin = 40

post_online = 0 # default 1. Change to 0 if you don't want to upload pics.
total_pics = 4 # number of pics to be taken
capture_delay = 4 # delay between pics
prep_delay = 2 # number of seconds at step 1 as users prep to have photo taken
restart_delay = 4 # how long to display finished message before beginning a new session

monitor_w = 800
monitor_h = 480
transform_x = 800 # how wide to scale the jpg when replaying
transfrom_y = 480 # how high to scale the jpg when replaying
offset_x = 0 # how far off to left corner to display photos
offset_y = 0 # how far off to left corner to display photos
replay_delay = 2 # how much to wait in-between showing pics on-screen after taking
replay_cycles = 1 # how many times to show each photo on-screen after taking

test_server = 'www.google.com'
real_path = os.path.dirname(os.path.realpath(__file__))


####################
### Other Config ###
####################
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # falling edge detection on button 1
#GPIO.setup(flash_pin,GPIO.IN)
 
#################
### Functions ###
#################

def cleanup():
  print('Ended abruptly')
  GPIO.cleanup()
atexit.register(cleanup)

def shut_it_down(channel):  
    print "Shutting down..." 
    time.sleep(3)
    os.system("sudo halt")

def exit_photobooth(channel):
    print "Photo booth app ended. RPi still running" 
    time.sleep(3)
    sys.exit()
          
def is_connected():
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(test_server)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False    

def init_pygame():
    pygame.init()
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    pygame.display.set_caption('Photo Booth Pics')
    pygame.mouse.set_visible(False) #hide the mouse cursor	
    return pygame.display.set_mode(size, pygame.FULLSCREEN)

def show_image(image_path):
    screen = init_pygame()
    img=pygame.image.load(image_path) 
    img = pygame.transform.scale(img,(transform_x,transfrom_y))
    screen.blit(img,(offset_x,offset_y))
    pygame.display.flip()

def display_pics(jpg_group):
    # this section is an unbelievable nasty hack - for some reason Pygame
    # needs a keyboardinterrupt to initialise in some limited circs (second time running)

    class Alarm(Exception):
        pass
    def alarm_handler(signum, frame):
        raise Alarm
    signal(SIGALRM, alarm_handler)
    alarm(3)
    try:
        screen = init_pygame()

        alarm(0)
    except Alarm:
        raise KeyboardInterrupt
    for i in range(0, replay_cycles): #show pics a few times
		for i in range(4): #show each pic
			filename = config.file_path + str(i) + '.jpg'
                        show_image(filename);
			time.sleep(replay_delay) # pause
		#show_image()

    
				
# define the photo taking function for when the big button is pressed 
def start_photobooth(): 
	################################# Begin Step 1 ################################# 
	show_image(real_path + "/blank.png")
	print "Get Ready"

	show_image(real_path + "/5.png")
	sleep(1)
	show_image(real_path + "/4.png")
	sleep(1)
	show_image(real_path + "/3.png")
	sleep(1)
	show_image(real_path + "/2.png")
	sleep(1)
	show_image(real_path + "/1.png")
	sleep(1)

	show_image(real_path + "/instructions.png")
	sleep(1.5)

	show_image(real_path + "/blank.png")
	
#	a = np.zeros((2464,3296, 3), dtype=np.uint8)
#	a = np.zeros((3296,2464, 3), dtype=np.uint8)
#	a[0:326, : ,:] = 0xff
#	a[2138:2464, : ,:] = 0xff
		

	camera = picamera.PiCamera()
	pixel_width = 3280 #1600 #use a smaller size to process faster, and tumblr will only take up to 500 pixels wide for animated gifs
	pixel_height =2464 #monitor_h * pixel_width // monitor_w
	camera.resolution = (pixel_width, pixel_height) 
	camera.vflip = False #True
	camera.hflip = False
	#camera.saturation = -100 # comment out this line if you want color images
	camera.start_preview()

#	o1 = camera.add_overlay(np.getbuffer(a), layer=3, alpha=255, fullscreen=False, window = (0, -400, 800, 100))	
#	o2 = camera.add_overlay(np.getbuffer(a), layer=3, alpha=255, fullscreen=False, window = (0, 2138, 3280, 352))	

#	sleep(2) #warm up camera

	################################# Begin Step 2 #################################
	print "Taking pics" 
	now = time.strftime("%H:%M:%S") #get the current date and time for the start of the filename
	try: #take the photos
		for i in range(4):
			sleep(capture_delay)
			camera.flash_mode = 'on'
			camera.capture(config.file_path +  str(i) + '.jpg')
	finally:
		camera.stop_preview()
		camera.close()

	try:
		display_pics(now)
	except Exception, e:
		tb = sys.exc_info()[2]
		traceback.print_exception(e.__class__, e, tb)
#	pygame.quit()
	print "Done"
	show_image(real_path + "/processing.png")
    	subprocess.call("sudo /home/pi/photobooth/assemble", shell=True)
	show_image(real_path + "/finished2.png")

	time.sleep(restart_delay)


	show_image(real_path + "/blank.png")

	show_image(real_path + "/intro.png");

####################
### Main Program ###
####################

show_image(real_path + "/intro.png");

while True:
        GPIO.wait_for_edge(button1_pin, GPIO.FALLING)
	time.sleep(0.2) #debounce
	start_photobooth()
