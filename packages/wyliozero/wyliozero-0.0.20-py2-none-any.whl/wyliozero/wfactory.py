from gpiozero.pins.rpigpio import RPiGPIOFactory, RPiGPIOPin
import winclude as w
import main as mainModule

def isRPI(x):
    return w.isR(x) or w.isButton(x) or w.isLED(x)

class WFactory(RPiGPIOFactory):

    def __init__(self):
        super(WFactory, self).__init__()
        self.pin_class = WPin

    def _to_gpio(self, spec):
        if isRPI(spec):
            return super(WFactory, self)._to_gpio(w.p(spec))
        elif spec in w.pinsAll:
            return spec

class WPin(RPiGPIOPin):
    def __init__(self, factory, number):
        #self._when_changed = None
        self._number = w.p(number)
        #self._when_changed_lock = None
        self.wnumber = number

        if isRPI(self.wnumber):
            super(WPin, self).__init__(factory, w.p(self.wnumber))
        elif w.isDPWM(self.wnumber):
            pass
        elif w.isD(self.wnumber):
            pass
        elif w.isA(self.wnumber):
            pass

    def close(self):
        if isRPI(self.wnumber):
            super(WPin, self).close()
        else:
            if w.isD(self.wnumber) and self._get_function() == 'o':
                mainModule.digitalWrite(self.wnumber, 0)

    def output_with_state(self, state):
        if isRPI(self.wnumber):
            super(WPin, self).output_with_state(state)
        else:
            mainModule.pinMode(self.wnumber, 'o')
            mainModule.digitalWrite(self.wnumber, state)

    def input_with_pull(self, pull):
        if isRPI(self.wnumber):
            super(WPin, self).input_with_pull(pull)
        else:
            mainModule.pinMode(self.wnumber, 'p')

    def _get_function(self):
        if isRPI(self.wnumber):
            return super(WPin, self)._get_function()
        else:
            return w.pinState[self.wnumber]

    def _set_function(self, value):
        if isRPI(self.wnumber):
            return super(WPin, self)._set_function(value)
        else:
            mainModule.pinMode(self.wnumber, value)

    def _get_state(self):
        if isRPI(self.wnumber):
            return super(WPin, self)._get_state()
        else:
            if (self._get_function() == 'o'):
                w.log.error('Trying to get state for pin {0} which is not set for INPUT'.format(self.wnumber))
            else:
                if w.isD(self.wnumber):
                    return mainModule.digitalRead(self.wnumber)
                elif w.isA(self.wnumber):
                    return mainModule.analogRead(self.wnumber)
    
    def _set_state(self, value):
        if isRPI(self.wnumber):
            super(WPin, self)._set_state(value)
        else:
            if (self._get_function() != 'o'):
                w.log.error('Trying to set state for pin {0} which is not set for OUTPUT'.format(self.wnumber))
            else:
                if value == int(value):
                    mainModule.digitalWrite(self.wnumber, value)
                else:
                    mainModule.analogWrite(self.wnumber, value* 255.0)

    def _get_pull(self):
        if isRPI(self.wnumber):
            return super(WPin, self)._get_pull()
        else:
            return w.pinState[self.wnumber] == 'p'

    def _set_pull(self, value):
        if isRPI(self.wnumber):
            return super(WPin, self)._set_pull(value)
        else:
            if (self._get_function() == 'o'):
                w.log.error('Trying to set pullup for pin {0} which is not set for INPUT'.format(self.wnumber))
            else:
                if value != 'up':
                    mainModule.pinMode(self.wnumber, 'i')
                else:
                    mainModule.pinMode(self.wnumber, 'p')


    def _get_frequency(self):
        if isRPI(self.wnumber):
            super(WPin, self)._get_frequency()
        else:
            pass
            print "unimplemented _get_frequency"

    def _set_frequency(self, value):
        if isRPI(self.wnumber):
            super(WPin, self)._set_frequency(value)
        else:
            pass
            print "unimplemented _set_frequency"

    def _get_bounce(self):
        super(WPin, self)._get_bounce()

    def _set_bounce(self, value):
        super(WPin, self)._set_bounce(value)

    def _get_edges(self):
        if isRPI(self.wnumber):
            super(WPin, self)._get_edges()
        else:
            return self._edges
            print "unimplemented _get_edges"

    def _set_edges(self, value):
        if isRPI(self.wnumber):
            super(WPin, self)._set_edges(value)
        else:
            f = self.when_changed
            self.when_changed = None
            try:
                self._edges = value
            finally:
                self.when_changed = f
            print "unimplemented _set_edges"

    def _call_when_changed(self, channel):
        super(WPin, self)._call_when_changed(channel)

    def _enable_event_detect(self):
        if isRPI(self.wnumber):
            super(WPin, self)._enable_event_detect()
        else:
            w.addCallback(self.wnumber, self._edges, callback=self._call_when_changed, bouncetime=self._bounce)
            print "unimplemented _enable_event_detect"

    def _disable_event_detect(self):
        if isRPI(self.wnumber):
            super(WPin, self)._disable_event_detect()
        else:
            w.removeCallback(self.wnumber)
            print "unimplemented _disable_event_detect"

    def _set_when_changed(self, value):
        if isRPI(self.wnumber):
            super(WPin, self)._set_when_changed(value)
        else:
            self._when_changed = value
            if hasattr(self, '_edges'):
                _edges = self._edges
            else:
                _edges = None

            if hasattr(self, '_bounce'):
                _bounce = self._bounce
            else:
                _bounce = None
            
            w.addCallback(self.wnumber, _edges, callback=value, bouncetime=_bounce)
            print "unimplemented _set_when_changed"
    
    def _get_when_changed(self):
        if isRPI(self.wnumber):
            return super(WPin, self)._get_when_changed()
        else:
            print "unimplemented _get_when_changed"
            if hasattr(self, '_when_changed'):
                print "pl"
                return self._when_changed
            else:
                print "nue"
                return None
            #w.removeCallback(self.wnumber)
            
        

