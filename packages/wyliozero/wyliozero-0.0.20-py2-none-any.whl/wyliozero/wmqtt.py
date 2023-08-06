import paho.mqtt.client as mqtt
import time
import subprocess
from os import environ as env
import json
from datetime import datetime

def getID():
    x = filter(lambda x : x.startswith('Serial'), subprocess.check_output(['cat','/proc/cpuinfo']).split('\n'))
    if len(x) > 0:
        return x[0].split(':')[1].strip().lstrip('0')
    else:
        return None

localdb = {}
localfn = {'update':{}, 'change':{}}
boardId = None


def putMessageInDb(topic, msg):
    if not localdb.has_key(topic):

        if localfn['change'].has_key(topic):
            localfn['change'][topic](msg)
    else:
        old = localdb[topic]
        if old != msg:

            if localfn['change'].has_key(topic):
                localfn['change'][topic](msg)


    if localfn['update'].has_key(topic):
        localfn['update'][topic](msg)

    
    localdb[topic] = msg
    



class ArgumentError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(ArgumentError, self).__init__(message)

class EnvironmentError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(EnvironmentError, self).__init__(message)


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Wmqtt(object):
    __metaclass__ = Singleton
    def __init__(self):
        self.initVars()
        self.connect()
        self.subscribePrivateAll()
        self.subscribePublicAll()

    def initVars(self):
        global boardId
        if env.has_key('BOARD_ID'):
            self.boardId = env['BOARD_ID']
        else:
            self.boardId = getID()
            if self.boardId == None:
                raise EnvironmentError("Error finding environment variable BOARD_ID")

        boardId = self.boardId

        if env.has_key('BROKER_ADDRESS'):
            self.brokerAddress = env['BROKER_ADDRESS']
        else:
            raise EnvironmentError("Error finding MQTT broker address from environment variable BROKER_ADDRESS")

        print 'Board ID', self.boardId
        print 'Broker address', self.brokerAddress

    
    def form(self, message):
        return json.dumps({'s':self.boardId, 'm':message, 't':datetime.now().strftime('%Y-%m-%d %H:%M:%S')})


    def on_message(self, client, userdata, messagejson):
        loaded = json.loads(str(messagejson.payload.decode('utf-8')))

        #s = loaded['s']
        message = loaded['m']
        #t = loaded['t']

        putMessageInDb(messagejson.topic, message)


    def connect(self):
        self.client = mqtt.Client(self.boardId)
        self.client.on_message=self.on_message
        self.client.connect(self.brokerAddress)

        self.client.loop_start()

        self.client.subscribe("broadcast")

    def subscribePrivateAll(self):
        self.client.subscribe('in' + '/' + self.boardId + '/' + '+')

    def unsubscribePrivateAll(self):
        self.client.unsubscribe('in' + '/' + self.boardId + '/' + '+')

    def subscribePrivate(self, topic='default'):
        self.client.subscribe('in' + '/' + self.boardId + '/' + topic)

    def unsubscribePrivate(self, topic='default'):
        self.client.unsubscribe('in' + '/' + self.boardId + '/' + topic)

    def sendPrivate(self, boardId, message, topic='default'):
        self.client.publish('in' + '/' + boardId + '/' + topic, self.form(message))

    

    def subscribePublicAll(self):
        self.client.subscribe('out' + '/' + '#')

    def unsubscribePublicAll(self):
        self.client.unsubscribe('out' + '/' + '#')

    def subscribePublic(self, boardId, topic='default'):
        self.client.subscribe('out' + '/' + boardId + '/' + topic)

    def unsubscribePublic(self, boardId, topic='default'):
        self.client.subscribe('out' + '/' + boardId + '/' + topic)

    def sendPublic(self, message, topic='default'):
        self.client.publish('out' + '/' + self.boardId + '/' + topic, self.form(message))



    def sendBroadcast(self, message):
        self.client.publish('broadcast', message)


class AwayInfo(object):
    def __init__(self, broadcast = False, public = False, private = False, who = None, topic = 'default' ):
        self._when_updated = None
        self._when_changed = None
        if broadcast == True:
            self.path = 'broadcast'
        else:
            if public == False and private == False:
                raise ArgumentError('Object AwayInfo must have either public = True or private = True, but not both at the same time')
            elif public == False and private == True:
                self.path = 'in' + '/' + boardId + '/' + topic
            elif public == True and private == False:
                if who == None:
                    raise ArgumentError('Object AwayInfo must have "who" argument set to awayBoardId if public = True')
                else:
                    self.path = 'out' + '/' + who + '/' + topic

            elif public == True and private == True:
                raise ArgumentError('Object AwayInfo must have either public = True or private = True, but not both at the same time')

    @property
    def values(self):
        while True:
            if localdb.has_key(self.path):
                yield localdb[self.path]

    @property
    def when_updated(self):
        return self._when_updated

    @when_updated.setter
    def when_updated(self, value):
        self._when_updated = value
        localfn['update'][self.path] = value

    @property
    def when_changed(self):
        return self._when_changed

    @when_changed.setter
    def when_changed(self, value):
        self._when_changed = value
        localfn['change'][self.path] = value

