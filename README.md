Chromecast companion
===

This is a dead project, the room concept is integrated into chrome2mqtt, and I made nodejs backend fir serving channel / xmltv data to my FrontEnd




*NOTE This is still in early concept state*

Companion program for chrome2mqtt. Arranges chromecasts into rooms, with one status per room. The status is updated from the chromecast that did the latest status update. 

Also the possibility to send a control command to a single room, which gets routed to the active chromecast in that room.

The concept is only tested with two chromecasts in each rom, one audio, and one clasic / video chromecast.

Naming convention for chromecasts
===
You need to name your chromecasts with a specific schema `<type>_<room>`, where type is either `tv` or `audio`, room name is anything you can imagine alfanumeric, like: livingroom, bedroom, bathroom1, bathroom2

Currently the program assumes that you have two chromecasts in each room. Things might explode if you try to play an audio/mp3 in a room, where you only have a clasic video chromecast device.

Channel list
===
The program includes a small webserver serving up channel data that can be played on the chromecasts. This is used in a dashboard project that I'm making. Channels can be supplemented with data from xmltv.

Format for channel list
---
Channels are listed in the file streams.json, each channel is described with the following data, which is sent directly to chrome2mqtt.

```json
{
    "link":"http://live-icy.gss.dr.dk/A/A03H.mp3",
    "friendly":"DR P1",
    "type":"audio/mp3",
    "xmlid":"p1.dr.dk",
    "icon": "someicon.png",
}
```

Icons can be served via http(s), or can be hosted elsewhere. Each icon is prefixed with the setting from commandline option `--host`, set it to a place where the icons is stored

see streams-example.json for formatting example
