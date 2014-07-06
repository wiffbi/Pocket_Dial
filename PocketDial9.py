1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
from __future__ import with_statement
import Live
#import time
import settings
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import MIDI_CC_TYPE 
from _Framework.EncoderElement import EncoderElement
 
from SessionControl import SessionControl
from MixerControl import MixerControl
from DeviceControl import DeviceControl
from TrackControl import TrackControl
 
 
class PocketDial(ControlSurface):
    __module__ = __name__
    __doc__ = "PocketDial MIDI Remote Script"
 
     
    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        #self.log_message(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------= PocketDial log opened =--------------")
 
        # turn off rebuild MIDI map until after setup
        #self._set_suppress_rebuild_requests(True)
        with self.component_guard():
            self._controls = [EncoderElement(MIDI_CC_TYPE, settings.CHANNEL, cc, settings.MAP_MODE) for cc in settings.CCS]
 
            mixer = MixerControl(self)
            session = SessionControl(self)
            device = DeviceControl(self)
            track = TrackControl(self)
         
            # bind mixer to session
            session.component.set_mixer(mixer.component)
            self.set_highlighting_session_component(session.component)
         
            # "magic" internal self._device_component, which enables lock to device, etc.
            self.set_device_component(device.component)
         
            # register components (Live 8 only?)
            #self._register_component(session.component)
            #self._register_component(mixer.component)
            #self._register_component(device.component)
             
         
            self._device = device
            self._track = track
 
        # turn rebuild back on
        #self._set_suppress_rebuild_requests(False)
     
    def get_encoder(self, bank, idx):
        #self.log_message("get encoder %d: CC: %d" % (bank*16 + idx, self._controls[bank*16 + idx].message_identifier()))
        return self._controls[bank*16 + idx]
     
    def _on_selected_track_changed(self):
        #ControlSurface._on_selected_track_changed(self)
        self._track._on_selected_track_changed()
        #pass
         
     
    def lock_to_device(self, device):
        ControlSurface.lock_to_device(self, device)
        self._device.lock_to_device(device)
 
    def unlock_from_device(self, device):
        ControlSurface.unlock_from_device(self, device)
        self._device.unlock_from_device(device)
