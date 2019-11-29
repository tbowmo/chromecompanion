"""
 Handles stream descriptors
"""
import hashlib
from json import loads, dumps
from chromecompanion.helpers.xmltv import xmltv

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
    icon = ""
    desc = ""
    category = ""
    type = "audio/mp3"
    def __init__(self, hostname='https://localhost:8181', **data):
        self.__dict__.update(data)
        if self.icon != '':
            self.icon = '{0}/channel/{1}'.format(hostname, self.icon)
        if self.friendly != "":
            self.id = hashlib.md5(self.friendly.encode('utf-8')).hexdigest()[:8]


class StreamData:
    """ Handles stream descriptors, searching and listing all channels """
    def __init__(self, channelFile, datafiles, hostname='https://localhost:8181'):
        self.datafiles = datafiles
        self.channels = []
        try:
            with open(channelFile) as streams_json:
                stdict = loads(streams_json.read())
                for st in stdict:
                    self.channels.append(Stream(hostname, **st))
        except IOError:
            pass

    def get_channel_list(self, media = "audio/mp3"):
        """ List all channels for given media, defaults to audio/mp3 """
        ret_ch = []
        for channel in self.channels :
            if channel.type == media:
                ret_ch.append(self.populate_channel(channel))
        return ret_ch

    def populate_channel(self, channel: Stream):
        if channel.xmlid != "":
            d = xmltv(channel.xmlid, self.datafiles)
            channel.programme = d.title()
            channel.start = d.start()
            channel.stop = d.stop()
            channel.desc = d.description()
            channel.category = d.category()
        return channel

    def get_channel_data(self, channelId=None):
        """ Get data for a single channel """
        try:
            ch = next(channel for channel in self.channels if channel.id == channelId or channel.link in channelId or channel.friendly == channelId)
            return self.populate_channel(ch)
        except Exception:
            pass
        return None

