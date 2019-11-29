import paho.mqtt.client as mqtt
import re
import logging
from os import path
import json
from types import SimpleNamespace as Namespace
from chromecompanion.stream import StreamData

class MQTT(mqtt.Client):
    is_connected = False
    root = ''
    def __init__(self, host='127.0.0.1', port=1883, client='chromecompanion', chrome2mqtt='chromecast', root='chromecompanion' , user=None, password=None, media: StreamData = None):
        super().__init__(host, port)
        self.streamData = media
        self.subscriptions = []
        self.host = host
        self.port = int(port)
        self.c2mqtt = chrome2mqtt
        self.root = root
        self.log = logging.getLogger('mqtt')
        self._client_id=client
        self.active_device = {}
        if (user is not None):
            self.username_pw_set(user, password)
        self.conn()

        # Subscribe to all relevant topics from chrome2mqtt
        self.message_callback_add('{0}/+/app'.format(self.c2mqtt), self.generic_topic)
        self.message_callback_add('{0}/+/state'.format(self.c2mqtt), self.generic_topic)
        self.message_callback_add('{0}/+/capabilities'.format(self.c2mqtt), self.generic_topic)
        self.message_callback_add('{0}/+/media'.format(self.c2mqtt), self.generic_topic)
        self.subscribe('{0}/+/+'.format(self.c2mqtt))

        self.message_callback_add('{0}/+/control/#'.format(self.root), self.control)
        self.subscribe('{0}/+/control/#'.format(root))

    def conn(self):
        self.connect(self.host, self.port, 30)
        self.loop_start()
        while not self.is_connected:
            pass

    def publish(self, topic, payload = None, qos = 0, retain=True):
        super().publish(topic, payload, qos, retain)
    
    def device(self, message):
        """ return room device is located in """
        regex = r"{0}\/(.*)_.*\/".format(self.c2mqtt)
        matches = re.search(regex, message.topic)
        assert matches != None, 'Could not get device from topic "{0}"'.format(message.topic)
        return matches.group(1)

    def room_message(self, message):
        """ return room device is located in """
        regex = r"{0}\/.*_(.*)\/".format(self.c2mqtt)
        matches = re.search(regex, message.topic)
        assert matches != None, 'Could not get room from topic "{0}"'.format(message.topic)
        return matches.group(1)

    def generic_topic(self, client, userdata, message):
        """ Generic topic handler, will copy the topic from chrome2mqtt to our own topic branch """
        room = self.room_message(message)
        msgtype = path.basename(path.normpath(message.topic))
        payload = message.payload
        if (msgtype == 'media'):
            payload = self.media_lookup(message.payload)
        self.publish('{0}/{1}/{2}'.format(self.root, room, msgtype), payload)
        self.publish('{0}/{1}/device'.format(self.root, room), self.device(message))
        self.active_device[room] = self.device(message)

    def media_lookup(self, media_payload):
        """ Media lookup, will return a json payload enriched with xmltv info, if available """
        payload = media_payload
        try:
            decoded = json.loads(payload.decode("utf-8"), object_hook=lambda d: Namespace(**d))
            decoded.type = 0
            media = self.streamData.get_channel_data(decoded.content_id)
            if (media is not None):
                decoded.title = media.desc
                decoded.artist = media.friendly
                decoded.album = media.programme
                decoded.album_art = media.icon
                decoded.type = 1
            payload = json.dumps(decoded, default=lambda o: o.__dict__)
        except:
            pass
        return payload

    def on_log(self, mqttc, obj, level, buf):
        self.log.debug(buf)

    def on_connect(self, mqttc, obj, flags, rc):
        if (rc == 0):
            self.is_connected = True

    def companion_room(self, message):
        '''Get the room name from our own topics'''
        regex = r"{0}\/(\w*)\/.*".format(self.root)
        matches = re.search(regex, message.topic)
        assert matches != None, 'Can not extract room name from topic "{0}"'.format(message.topic)
        return matches.group(1)

    def control(self, client, userdata, message):
        regex = r".*\/control\/(.*)".format(self.root)
        matches = re.search(regex, message.topic, re.MULTILINE)
        command = matches.group(1)        
        if (command == 'play'):
            return self.playHandler(client, userdata, message)
        room = self.companion_room(message)
        activeDevice = self.active_device[room]
        topic = '{0}/{1}_{2}/control/{3}'.format(self.c2mqtt, activeDevice, room, command)
        self.publish(topic, message.payload)

    def playHandler(self, client, userdata, message):
        try:
            room = self.companion_room(message)
            media = json.loads(message.payload.decode("utf-8"), object_hook=lambda d: Namespace(**d))
            device = 'tv'
            if hasattr(media, 'type') and media.type.lower() == 'audio/mp3':
                device = 'audio'
            topic = '{0}/{1}_{2}/control/play'.format(self.c2mqtt, device, room)
            if (device != self.active_device):
                self.publish('{0}/{1}_{2}/control/quit'.format(self.c2mqtt, self.active_device[room], room), '')
            self.publish(topic, message.payload)
        except:
            pass
