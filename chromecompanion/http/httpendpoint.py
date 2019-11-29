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
    if type=='radio': 
        od = mediaStore.get_channel_list()
    else:
        od = mediaStore.get_channel_list('video/mp4')
    return json.dumps(od, default=lambda o: o.__dict__)

@bottle.get('/channel/<logo>')
def logo(logo):
    return bottle.static_file(logo, root='images/')   
 
def runHttpEndpoint(bindAddress='0.0.0.0', port='8181', corsDomain='*', media: StreamData = None):
    global mediaStore
    mediaStore = media
    APP = application = bottle.default_app()
    application.install(cors(corsDomain))
    APP.run(host=bindAddress, port=port)

