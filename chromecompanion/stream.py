"""
 Handles stream descriptors
"""
import hashlib
from json import loads, dumps
from chromecompanion.helpers.xmltv import xmltv

class StreamData:
    """ Handles stream descriptors, searching and listing all channels """
    def __init__(self, channelFile, datafiles):
        self.datafiles = datafiles
        self.channels = []
        try:
            with open(channelFile) as streams_json:
                stdict = loads(streams_json.read())
                for st in stdict:
                    self.channels.append(Stream(**st))
        except IOError:
            pass

    def get_channel_list(self, media = "audio/mp3"):
        """ List all channels for given media, defaults to audio/mp3 """
        ret_ch = []
        for channel in self.channels :
            if channel.type == media:
                if channel.xmlid != "":
                    d = xmltv(channel.xmlid, self.datafiles)
                    channel.programme = d.title()
                    channel.start = d.start()
                    channel.stop = d.stop()
                ret_ch.append(channel)
        return ret_ch

    def get_channel_data(self, channelId=None, link=None, ch=None):
        """ Get data for a single channel """
        try:
            for channel in self.channels:
                if channelId is not None:
                    if channel.id == channelId:
                        return channel
                if link is not None:
                    if channel.link in link:
                        return channel
                if ch is not None:
                    if channel.friendly == ch:
                        return channel
        except Exception:
            pass
        dummy = {'friendly':'', 'media':''}
        return Stream(**dummy)

class Stream:
    """ Single streaming channel data """
    programme = ""
    start = ""
    stop = ""
    id = ""
    friendly = ""
    extra = ""
    xmlid = ""
    link = ""
    type = "audio/mp3"
    def __init__(self, **data):
        self.__dict__.update(data)
        if self.friendly != "":
            self.id = hashlib.md5(self.friendly.encode('utf-8')).hexdigest()[:8]

1
