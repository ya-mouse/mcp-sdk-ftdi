#!/bin/sh -e

sigstop()
{
    echo "Interrupted."
    trap - EXIT TERM KILL INT QUIT
    rm -f $PWD/lock-ftdi-B.lck
    kill -9 $lckpid 2>/dev/null ||:
}

trap sigstop EXIT TERM KILL INT QUIT

# Wait for ttyUSBx exclusive availability
! lsmod | fgrep -q ftdi_sio ||
    while ! rmmod ftdi_sio; do sleep 1; done

# Count ttyUSBx devices before installing module
cnt="$(ls -1 /dev/ttyUSB* 2>/dev/null | wc -l || echo 0)"

# Lock PicoTAP USB channel
rm -f $PWD/lock-ftdi-B.lck
LD_LIBRARY_PATH=$PWD python lock-ftdi-B.py &
lckpid=$!

# Wait for lock file
retry=0
while [ ! -e $PWD/lock-ftdi-B.lck -a $retry -lt 10 ]; do
    sleep 1
    retry=$((retry+1))
done

if [ $retry = 10 ]; then
    echo "Unable to lock 'Dual RS232-HS B'."
    exit 1
fi

rm -f $PWD/lock-ftdi-B.lck

# Create ttyUSBx for USB serial channel
modprobe ftdi_sio

retry=0
while [ "$(ls -1 /dev/ttyUSB* 2>/dev/null | wc -l || echo 0)" -le "$cnt" -a $retry -lt 10 ]; do
    sleep 1
done

trap - EXIT TERM KILL INT QUIT

kill $lckpid
wait $lckpid ||:
