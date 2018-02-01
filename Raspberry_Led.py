#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
 
BIT0 = 24
BIT1 = 5
BIT2 = 6
BIT3 = 26

segCode = [0xc0,0xf9,0xa4,0xb0,0x99,0x92,0x82,0xf8,0x80,0x90]  #0~9
pins = [19,22,12,20,21,13,25,16,26,6,5,24]
bits = [BIT0, BIT1, BIT2, BIT3]

def print_msg():
  print 'Program is running...'
  print 'Please press Ctrl+C end the program...'

def digitalWriteByte(val):
  GPIO.output(19, val & (0x01 << 0))
  GPIO.output(22, val & (0x01 << 1))
  GPIO.output(12, val & (0x01 << 2))
  GPIO.output(20, val & (0x01 << 3))
  GPIO.output(21, val & (0x01 << 4))
  GPIO.output(13, val & (0x01 << 5))
  GPIO.output(25, val & (0x01 << 6))
  GPIO.output(16, val & (0x01 << 7))

def display_1(): 
  show()
  for i in range(10):
    digitalWriteByte(segCode[i])
    time.sleep(0.2)
  hide()

def hide():
  GPIO.output(BIT0, GPIO.LOW) 
  GPIO.output(BIT1, GPIO.LOW) 
  GPIO.output(BIT2, GPIO.LOW) 
  GPIO.output(BIT3, GPIO.LOW) 

def show():
  GPIO.output(BIT0, GPIO.HIGH) 
  GPIO.output(BIT1, GPIO.HIGH) 
  GPIO.output(BIT2, GPIO.HIGH) 
  GPIO.output(BIT3, GPIO.HIGH) 
  
def showNum(bit,num):
  hide()
  GPIO.output(bits[bit], GPIO.HIGH)
  digitalWriteByte(segCode[num])
  time.sleep(0.005)

def display_3(num):
  b0 = num % 10
  b1 = num % 100 / 10 
  b2 = num % 1000 / 100
  b3 = num / 1000

  if num < 10:
    showNum(0,b0)

  elif num >= 10 and num < 100:
    showNum(0,b0)
    showNum(1,b1)
  elif num >= 100 and num < 1000:
    showNum(0,b0)
    showNum(1,b1)
    showNum(2,b2)
  elif num >= 1000 and num < 10000:
    showNum(0,b0)
    showNum(1,b1)
    showNum(2,b2)
    showNum(3,b3)
  else:
    print 'Out of range, num should be 0~9999 !'

def setup():
  #GPIO.setmode(GPIO.BOARD)    #Number GPIOs by its physical location
  GPIO.setmode(GPIO.BCM)
  for pin in pins:
    GPIO.setup(pin, GPIO.OUT)    #set all pins' mode is output
    GPIO.output(pin, GPIO.HIGH)  #set all pins are high level(3.3V)

def loop():
  while True:
    print_msg()
    display_1()
    time.sleep(1)

    tmp = int(raw_input('Please input a num(0~9999):'))
    for i in range(500):
      display_3(tmp)
    time.sleep(1)


def destroy():   #When program ending, the function is executed. 
  for pin in pins:  
    GPIO.output(pin, GPIO.LOW) #set all pins are low level(0V) 
    GPIO.setup(pin, GPIO.IN)   #set all pins' mode is input
   
if __name__ == '__main__': #Program starting from here 
  setup() 
  try:
    loop()
	 
  except KeyboardInterrupt:  
    destroy()
