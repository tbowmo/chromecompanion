from chromecompanion.stream import StreamData
import json
from chromecompanion.http.cors import cors
import bottle

mediaStore = None

@bottle.get('/<type>/list')
def medialist(type):
    od = None
    if mediaStore == None:
        return '[]'
    if type=='audio': 
        od = mediaStore.get_channel_list()
    else:
        od = mediaStore.get_channel_list('video/mp4')
    print(od)
    return json.dumps(od, default=lambda o: o.__dict__)

def runHttpEndpoint(bindAddress='0.0.0.0', port='8181', media: StreamData = None):
    global mediaStore
    mediaStore = media
    APP = application = bottle.default_app()
    application.install(cors())
    APP.run(host=bindAddress, port=port)

