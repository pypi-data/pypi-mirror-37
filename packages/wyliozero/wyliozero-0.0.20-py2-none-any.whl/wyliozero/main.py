import winclude as w
from gpiozero import *
from wmqtt import Wmqtt as LabNetwork, AwayInfo
from wlcd import lcd as LabLCD

Device.pin_factory = w.wfactory.WFactory()

def pause():
    print "Press Enter to end the program"
    raw_input()
    w._exit(0)


for eachPin in w.pinsAll:
    globals()[eachPin] = eachPin

class DHTsensor:
    def __init__(self, pin):
        self.pin = pin
        
    def humidityRead(self):
        return humidityRead(self.pin)

    def temperatureRead(self):
        return temperatureRead(self.pin)



def humidityRead(pin):
    if w.isR(pin):
        x, y = w.DHT_read_retry(11,w.p(pin))
        return x
    elif w.isD(pin) or w.isA(pin) or w.isAdig(pin) or w.isButton(pin) or w.isLED(pin):
        w.log.error('Pin {0} cannot be used to read humidity from it'.format(pin))
    else:
        w.log.error(pin, 'arg')


def temperatureRead(pin):
    if w.isR(pin):
        x, y = w.DHT_read_retry(11,w.p(pin))
        return y
    elif w.isD(pin) or w.isA(pin) or w.isAdig(pin) or w.isButton(pin) or w.isLED(pin):
        w.log.error('Pin {0} cannot be used to read temperature from it'.format(pin))
    else:
        w.log.error(pin, 'arg')

INPUT = 'i'
OUTPUT = 'o'

HIGH = 1
LOW = 0

def pinMode(pin, value):
    if w.isR(pin):
        pass

    elif w.isDPWM(pin):
        if w.isOutput(value):
            w.ard.set_pin_mode(w.p(pin), w.ard.PWM, w.ard.DIGITAL)
        elif w.isInput(value):
            w.ard.set_pin_mode(w.p(pin), w.ard.INPUT, w.ard.DIGITAL)
        elif w.isPullupInput(value):
            w.ard.set_pin_mode(w.p(pin), w.ard.PULLUP, w.ard.DIGITAL)
        else:
            w.log.error(value, 'arg')

    elif w.isD(pin):
        if w.isOutput(value):
            w.ard.set_pin_mode(w.p(pin), w.ard.OUTPUT, w.ard.DIGITAL)
        elif w.isInput(value):
            w.ard.set_pin_mode(w.p(pin), w.ard.INPUT, w.ard.DIGITAL)
        elif w.isPullupInput(value):
            w.ard.set_pin_mode(w.p(pin), w.ard.PULLUP, w.ard.DIGITAL)
        else:
            w.log.error(value, 'arg')

    elif w.isA(pin):
        if w.isOutput(value):
            w.log.error('Analog pin {0} cannot be set as OUTPUT'.format(pin))
        elif w.isInput(value):
            w.ard.set_pin_mode(w.p(pin), w.ard.INPUT, w.ard.ANALOG)
        elif w.isPullupInput(value):
            w.ard.set_pin_mode(w.p(pin), w.ard.PULLUP, w.ard.ANALOG)
        else:
            w.log.error(value, 'arg')

    elif w.isAdig(pin):
        if w.isOutput(value):
            w.ard.set_pin_mode(w.p(pin), w.ard.OUTPUT, w.ard.DIGITAL)
        elif w.isInput(value):
            w.ard.set_pin_mode(w.p(pin), w.ard.INPUT, w.ard.DIGITAL)
        elif w.isPullupInput(value):
            w.ard.set_pin_mode(w.p(pin), w.ard.PULLUP, w.ard.DIGITAL)
        else:
            w.log.error(value, 'arg')

    elif w.isButton(pin):
        if w.isOutput(value):
            w.log.error('Button pin {0} cannot be set as OUTPUT'.format(pin))
        elif w.isInput(value):
            pass
        elif w.isPullupInput(value):
            pass
        else:
            w.log.error(value, 'arg')

    elif w.isLED(pin):
        if w.isOutput(value):
            pass
        elif w.isInput(value):
            w.log.error('LED pin {0} cannot be set as INPUT'.format(pin))
        elif w.isPullupInput(value):
            w.log.error('LED pin {0} cannot be set as INPUT'.format(pin))
        else:
            w.log.error(value, 'arg')

    else:
        w.log.error(pin, 'arg')

    m = w.transformMode(value)
    if m != None:
        w.pinState[pin] = m



def digitalWrite(pin, value):
    if w.isR(pin):
        if w.isPinOutput(pin):
            if w.isLow(value):
                x = w.rpi.OutputDevice(w.p(pin), pin_factory=w.defaultFactory)
                x.off()
                x.close()
            elif w.isHigh(value):
                x = w.rpi.OutputDevice(w.p(pin), pin_factory=w.defaultFactory)
                x.on()
                x.close()
            else:
                w.log.error(value, 'arg')
        else:
            w.log.error('Raspberry pin {0} must be set as OUTPUT for digitalWrite'.format(pin))

    elif w.isDPWM(pin):
        if w.isPinOutput(pin):
            if w.isLow(value):
               w.ard.analog_write(w.p(pin), 0)
            elif w.isHigh(value):
                w.ard.analog_write(w.p(pin), 255)
            else:
                w.log.error(value, 'arg')
        else:
            w.log.error('Pin {0} must be set as OUTPUT for digitalWrite'.format(pin))

    elif w.isD(pin) or w.isAdig(pin):
        if w.isPinOutput(pin):
            if w.isLow(value):
               w.ard.digital_write(w.p(pin), 0)
            elif w.isHigh(value):
                w.ard.digital_write(w.p(pin), 1)
            else:
                w.log.error(value, 'arg')
        else:
            w.log.error('Pin {0} must be set as OUTPUT for digitalWrite'.format(pin))

    elif w.isA(pin):
        w.log.error('Analog pin {0} cannot be used for digitalWrite'.format(pin))

    elif w.isButton(pin):
        w.log.error('Button pin {0} cannot be used for digitalWrite'.format(pin))

    elif w.isLED(pin):
        if w.isPinOutput(pin):
            if w.isLow(value):
                x = w.rpi.OutputDevice(w.p(pin), pin_factory=w.defaultFactory)
                x.off()
                x.close()
            elif w.isHigh(value):
                x = w.rpi.OutputDevice(w.p(pin), pin_factory=w.defaultFactory)
                x.on()
                x.close()
            else:
                w.log.error(value, 'arg')
        else:
            w.log.error('LED pin {0} must be set as OUTPUT for digitalWrite'.format(pin))

    else:
        w.log.error(pin, 'arg')



def digitalRead(pin):
    if w.isR(pin):
        if w.isPinInput(pin):
            x = w.rpi.InputDevice(w.p(pin), False, pin_factory=w.defaultFactory)
            v = x.value
            x.close()
            if v: return 1
            else: return 0
        elif w.isPinPullupInput(pin):
            x = w.rpi.InputDevice(w.p(pin), True, pin_factory=w.defaultFactory)
            v = x.value
            x.close()
            if v: return 1
            else: return 0
        else:
            w.log.error('Raspberry pin {0} must be set as INPUT for digitalRead'.format(pin))
    
    elif w.isD(pin) or w.isAdig(pin):
        v = w.ard.digital_read(w.p(pin))
        if (v): return 1
        else: return 0

    elif w.isA(pin):
        w.log.error('Analog pin {0} cannot be used for digitalRead'.format(pin))

    elif w.isButton(pin):
        if w.isPinInput(pin):
            x = w.rpi.InputDevice(w.p(pin), False, pin_factory=w.defaultFactory)
            v = x.value
            x.close()
            if v: return 1
            else: return 0
        elif w.isPinPullupInput(pin):
            x = w.rpi.InputDevice(w.p(pin), True, pin_factory=w.defaultFactory)
            v = x.value
            x.close()
            if v: return 1
            else: return 0
        else:
            w.log.error('Button pin {0} must be set as INPUT for digitalRead'.format(pin))

    elif w.isLED(pin):
        w.log.error('LED pin {0} cannot be used for digitalRead'.format(pin))

    else:
        w.log.error(pin, 'arg')


def analogRead(pin):
    if w.isR(pin):
        w.log.error('Raspberry pin {0} cannot be used for analogRead'.format(pin))
    
    elif w.isD(pin) or w.isAdig(pin):
        w.log.error('Digital pin {0} cannot be used for analogRead'.format(pin))

    elif w.isA(pin):
        if w.isPinInput(pin) or w.isPinPullupInput(pin):
            return w.ard.analog_read(w.p(pin))
        else:
            w.log.error('Analog pin {0} must be set as INPUT for analogRead'.format(pin))

    elif w.isButton(pin):
        w.log.error('Button pin {0} cannot be used for analogRead'.format(pin))
    elif w.isLED(pin):
        w.log.error('LED pin {0} cannot be used for analogRead'.format(pin))
    else:
        w.log.error(pin, 'arg')


def analogWrite(pin, value):
    if w.isDPWM(pin):
        if w.isPinOutput(pin):
            value = int(value)
            if 0 <= value <= 255:
                w.ard.analog_write(w.p(pin), value)
            else:
                w.log.error('Argument value "{0}" must be a number between 0 and 255'.format(value))
            
        else:
            w.log.error('Pin {0} must be set as OUTPUT for analogWrite'.format(pin))

    elif w.isD(pin) or w.isAdig(pin) or w.isR(pin) or w.isA(pin) or w.isButton(pin) or w.isLED(pin):
        w.log.error('Pin {0} cannot be used for analogWrite'.format(pin))

    else:
        w.log.error(w.p(pin), 'arg')

