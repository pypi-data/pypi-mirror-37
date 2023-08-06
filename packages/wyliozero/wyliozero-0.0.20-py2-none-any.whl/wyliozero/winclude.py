import gpiozero as rpi
from PyMata.pymata import PyMata
from Adafruit_DHT import read_retry as DHT_read_retry
from os import _exit

import wfactory
from gpiozero.pins.rpigpio import RPiGPIOFactory
import sys

defaultFactory = RPiGPIOFactory()


class DHTsensor:
    def __init__(self, pin):
        self.pin = pin

    def humidityRead(self):
        return DHT_read_retry(11, self.pin)[0]

    def temperatureRead(self):
        return DHT_read_retry(11, self.pin)[1]

from serial.serialutil import SerialException
print "Starting program..."
serialTry = ["/dev/serial0"]
ard = None
for tries in serialTry:
    try:
        ard = PyMata(tries, verbose=False)
    except SerialException:
        pass
    else:
        break

if ard == None:
    raise SerialException("No available serial found for Firmata")



def excepthook(type, value, traceback):
    sys.stderr.write(str(value) + '\n')
    sys.stderr.flush()

sys.excepthook = excepthook


class Log():
    def __init__(self):
        pass
    def error(self, s, reason = None):
        if reason == 'arg':
            txt = 'ERROR "{0}" argument is not correct'.format(s)
            #import traceback
            #traceback.print_stack()
        else:
            txt = 'ERROR ' + str(s)
        raise SystemError(txt)
    def info(self, s):
        print 'INFO ' + str(s)

log = Log()

pins = {
    'R':['R4','R17','R27','R22','R10','R9','R11','R18','R23','R8','R7'],
    'D':['D2','D3','D4','D5','D6','D7','D8','D9','D10','D11','D12','D13'],
    'A':['A0','A1','A2','A3','A4','A5','A6'],
    'Adig':['D14','D15','D16','D17','D18','D19','D20'],
    'Button':['R13','R19'],
    'LED':['R20','R21']
}

pinsAll = []
pinsAll.extend(pins['R'])
pinsAll.extend(pins['D'])
pinsAll.extend(pins['A'])
pinsAll.extend(pins['Adig'])
pinsAll.extend(pins['Button'])
pinsAll.extend(pins['LED'])



pinState = {k:None for k in pinsAll}

def isR(pin):
    return (pin in pins['R']) or (('R' + str(pin)) in pins['R'])

def isD(pin):
    return pin in pins['D']

def isDPWM(pin):
    return pin in ['D3','D5','D6','D9','D10','D11']

def isA(pin):
    return pin in pins['A']

def isAdig(pin):
    return pin in pins['Adig']

def isButton(pin):
    return (pin in pins['Button']) or (('R' + str(pin)) in pins['Button'])

def isLED(pin):
    return (pin in pins['LED']) or (('R' + str(pin)) in pins['LED'])

def isLow(value):
    return value in ['0', 0, 'LOW', False]

def isHigh(value):
    return value in ['1', 1, 'HIGH', True]

def isOutput(value):
    if not (isinstance(value,str) or isinstance(value,unicode)):
        return False
    value = value.lower()
    return value in ['out','output','o']

def isInput(value):
    if not (isinstance(value,str) or isinstance(value,unicode)):
        return False
    value = value.lower()
    return value in ['in','input','i']

def isPullupInput(value):
    if not (isinstance(value,str) or isinstance(value,unicode)):
        return False
    value = value.lower()
    return value in ['input_pullup','inputpullup','pullup_input','pullupinput','pull','pullup','p']

def isPinOutput(pin):
    return pinState[pin] == 'o'

def isPinInput(pin):
    return pinState[pin] == 'i'

def isPinPullupInput(pin):
    return pinState[pin] == 'p'

def transformMode(value):
    if isInput(value):
        return 'i'
    if isOutput(value):
        return 'o'
    if isPullupInput(value):
        return 'p'
    return None

def p(pin):
    if isinstance(pin, int):
        return pin
    elif isD(pin) or isA(pin):
        return int(pin[1:])
    else:
        if pin[0] == 'R':
            return int(pin[1:])
        else:
            return int(pin)

def addCallback(pin, edges, callback, bouncetime):

    def ccb(a1):
        callback()



    if pinState[pin] == 'o':
        log.error('Cannot add callback to pin {0} because it must be set to INPUT'.format(pin))
    else:
        if isR(pin):
            log.error('Cannot add callback to pin {0} because R pins cannot be set this way'.format(pin))

        elif isD(pin):
            if pinState[pin] == 'i':
                ard.set_pin_mode(p(pin), ard.INPUT, ard.DIGITAL, ccb)
            elif pinState[pin] == 'p':
                ard.set_pin_mode(p(pin), ard.PULLUP, ard.DIGITAL, ccb)

        elif isA(pin):
            if pinState[pin] == 'i':
                ard.set_pin_mode(p(pin), ard.INPUT, ard.ANALOG, ccb)
            elif pinState[pin] == 'p':
                ard.set_pin_mode(p(pin), ard.PULLUP, ard.ANALOG, ccb)

        else:
            log.error(pin, 'arg')


def removeCallback(pin):
    if pinState[pin] == 'o':
        log.error('Cannot remove callback from pin {0} because it must be set to INPUT'.format(pin))
    else:
        if isR(pin):
            log.error('Cannot remove callback from pin {0} because R pins cannot be unset this way'.format(pin))

        elif isD(pin):
            if pinState[pin] == 'i':
                ard.set_pin_mode(p(pin), ard.INPUT, ard.DIGITAL)
            elif pinState[pin] == 'p':
                ard.set_pin_mode(p(pin), ard.PULLUP, ard.DIGITAL)

        elif isA(pin):
            if pinState[pin] == 'i':
                ard.set_pin_mode(p(pin), ard.INPUT, ard.ANALOG)
            elif pinState[pin] == 'p':
                ard.set_pin_mode(p(pin), ard.PULLUP, ard.ANALOG)

        else:
            log.error(pin, 'arg')
