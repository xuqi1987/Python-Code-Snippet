#! /usr/bin/python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time

def checkdist():

    #发出触发信号
    GPIO.output(21,GPIO.HIGH)
    #保持10us以上（我选择15us）
    time.sleep(0.000015)
    GPIO.output(21,GPIO.LOW)
    while not GPIO.input(20):
        pass
    #发现高电平时开时计时
    t1 = time.time()
    while GPIO.input(20):
        pass
    #高电平结束停止计时
    t2 = time.time()
    #返回距离，单位为米
    return (t2-t1)*340/2

GPIO.setmode(GPIO.BCM)
#第21号针，GPIO21
GPIO.setup(21,GPIO.OUT,initial=GPIO.LOW)
#第20号针，GPIO20
GPIO.setup(20,GPIO.IN)

time.sleep(2)
try:
    while True:
    	print 'Distance: %0.2f m' %checkdist()
    	time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
