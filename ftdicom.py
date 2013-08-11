#!/usr/bin/python

import sys
import tty
import termios
import select
from time import sleep

try:
    import ftd2xx
except OSError:
    print "Check libftd2xx.so presence."
    sys.exit(2)

try:
    com = ftd2xx.openEx('Dual RS232-HS A', ftd2xx.ftd2xx.OPEN_BY_DESCRIPTION)
except ftd2xx.ftd2xx.DeviceError:
    print "Unable to open 'Dual RS232-HS A'."
    sys.exit(1)
except:
    print "Unknown error while openning 'Dual RS232-HS A'."
    sys.exit(3)

com.setBaudRate(ftd2xx.ftd2xx.BAUD_38400)
com.setDataCharacteristics(ftd2xx.ftd2xx.BITS_8, ftd2xx.ftd2xx.STOP_BITS_1, ftd2xx.ftd2xx.PARITY_NONE)
com.setFlowControl(ftd2xx.ftd2xx.FLOW_NONE)

old_settings = termios.tcgetattr(sys.stdin)
try:
    tty.setcbreak(sys.stdin.fileno())

    while True:
        cnt = com.getQueueStatus()
        if select.select([sys.stdin],[],[],0) == ([sys.stdin], [], []):
            input = sys.stdin.read(1)
            com.write(input)
        elif cnt != 0:
            print com.read(cnt, False) # for non-RAW input pass "False" as second argument

finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

com.close()
