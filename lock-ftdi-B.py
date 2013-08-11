#!/usr/bin/python

from sys import exit
from time import sleep

try:
    import ftd2xx
except OSError:
    print "Check libftd2xx.so presence."
    exit(2)

try:
    com = ftd2xx.openEx('Dual RS232-HS B', ftd2xx.ftd2xx.OPEN_BY_DESCRIPTION)
except ftd2xx.ftd2xx.DeviceError:
    print "Unable to open 'Dual RS232-HS B'."
    exit(1)
except:
    print "Unknown error while openning 'Dual RS232-HS B'."
    exit(3)

open('lock-ftdi-B.lck', 'w').close()

while True:
    cnt = com.getQueueStatus()
    com.read(cnt)
    sleep(1)

com.close()
