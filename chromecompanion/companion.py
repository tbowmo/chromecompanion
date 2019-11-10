from chromecompanion.http.httpendpoint import runHttpEndpoint
from chromecompanion.mqtt import MQTT
import logging
from chromecompanion.stream import StreamData
import logging.config
import logging
import socket
import signal
import sys
from os import path

__version__ = __VERSION__ = "1.0.0"

def parse_args(argv = None):
    import argparse
    parser = argparse.ArgumentParser(prog='chrome2mqtt',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='chrome2mqtt\n\nConnects your chromecasts to your mqtt-broker',
        epilog='See more on https://github.com/tbowmo/chrome2mqtt/README.md'
        )
    parser.add_argument('--mqttport', action="store", default=1883, type=int, help="MQTT port on host")
    parser.add_argument('--mqttclient', action="store", default=socket.gethostname(), help="Client name for mqtt")
    parser.add_argument('--mqttroot', action="store", default="chromecast", help="MQTT root topic")
    parser.add_argument('--mqttuser', action="store", default=None, help="MQTT user (if authentication is enabled for your broker)")
    parser.add_argument('--mqttpass', action="store", default=None, help="MQTT password (if authentication is enabled for your broker)")
    parser.add_argument('--chrome2mqtt', action="store", default="chrome2mqtt", help="Root topic for chrome2mqtt")
    parser.add_argument('-H', '--mqtthost', action="store", default="127.0.0.1", help="MQTT Host")
    parser.add_argument('-l', '--logfile', action="store", default=None, help="Log to filename")
    parser.add_argument('-d', '--debug', action="store_const", dest="log", const=logging.DEBUG, help="loglevel debug")
    parser.add_argument('-v', '--verbose', action="store_const", dest="log", const=logging.INFO, help="loglevel info")
    parser.add_argument('-V', '--version', action='version', version='%(prog)s {version}'.format(version=__VERSION__))
    parser.add_argument('-C', '--cleanup', action="store_true", dest="cleanup", help="Cleanup mqtt topic on exit")

    return parser.parse_args(argv)


def setup_logging(
        file = None, 
        level=logging.WARNING
    ):
    if (path.isfile('./logsetup.json')):
        with open('./logsetup.json', 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    elif (file != None):
        logging.basicConfig(level=level,
                            filename=file,
                            format = '%(asctime)s %(name)-16s %(levelname)-8s %(message)s')
    else:
        logging.basicConfig(level=level,
                            format = '%(asctime)s %(name)-16s %(levelname)-8s %(message)s')

media = StreamData('./streams.json', './xmltv')

def main_loop():
    args = parse_args()

    setup_logging(args.logfile, args.log)
    
    def signal_handler(sig, frame):
        print('Shutting down')
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    client = MQTT(host='192.168.1.64', root='media', media=media)
    runHttpEndpoint(media=media)

