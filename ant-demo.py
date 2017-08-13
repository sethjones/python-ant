# Python 2
# ANT+ HRM Demo Script for Python-ANT.  Based on demo scripts provided with library.
import sys
import time
import datetime
import usb.core
import usb.util

from ant.core import driver, node, event, message, log
from ant.core.constants import CHANNEL_TYPE_TWOWAY_RECEIVE, TIMEOUT_NEVER
from datetime import datetime

SERIAL = '/dev/ttyUSB0'
NETKEY = '\xB9\xA5\x21\xFB\xBD\x72\xC3\x45'
# Variables for defining valid heart rate range.
hrHigh = 150
hrLow = 50

# Verify that ANT+ USB is plugged in.
dev = usb.core.find(idVendor=0x0fcf, idProduct=0x1008)
# Generate error if device is not found.
if dev is None:
    raise ValueError('ANT+ USB Device not found')

class HRM(event.EventCallback):

    def __init__(self, serial, netkey):
        self.serial = serial
        self.netkey = netkey
        self.antnode = None
        self.channel = None

    def start(self):
        print("Starting ANT+ node")
        self._start_antnode()
        self._setup_channel()
        self.channel.registerCallback(self)
        print("Listening for hr events")

    def stop(self):
        if self.channel:
            self.channel.close()
            self.channel.unassign()
        if self.antnode:
            self.antnode.stop()

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.stop()

# Use USB2 driver to prevent error.  There currently is an issue where nodes sometimes fails to start.
    def _start_antnode(self):
        stick = driver.USB2Driver(self.serial)
        self.antnode = node.Node(stick)
        self.antnode.start()
        #Added for debug
        print("ANT+ node started.")

    def _setup_channel(self):
        key = node.NetworkKey('N:ANT+', self.netkey)
        self.antnode.setNetworkKey(0, key)
        self.channel = self.antnode.getFreeChannel()
        self.channel.name = 'C:HRM'
        self.channel.assign('N:ANT+', CHANNEL_TYPE_TWOWAY_RECEIVE)
        #ID is specific to HRM devices.
        self.channel.setID(120, 0, 0)
        self.channel.setSearchTimeout(TIMEOUT_NEVER)
        self.channel.setPeriod(8070)
        self.channel.setFrequency(57)
        self.channel.open()
        #Added for debug
        print("ANT+ channel open.")

    def process(self, msg):
        if isinstance(msg, message.ChannelBroadcastDataMessage):
                hr = ord(msg.payload[-1])
                print("Heart rate is {}".format(hr))
                with open("Output.txt", "a") as text_file:
                        text_file.write("Heart Rate: {} | Datetime: {}\n".format(ord(msg.payload[-1]), str(datetime.now())))
                # Specific alert for if heart rate is out of range.
                if hr not in range(hrLow,hrHigh):
                    print("HEART RATE OUT OF RANGE!\n")
                    with open("Output.txt", "a") as text_file:
                        text_file.write("Heart Rate out of range!\n")
with HRM(serial=SERIAL, netkey=NETKEY) as hrm:
    hrm.start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(0)