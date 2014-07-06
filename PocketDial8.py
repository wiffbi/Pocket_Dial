import Live
#import time
import settings
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import MIDI_CC_TYPE 
from _Framework.EncoderElement import EncoderElement
#from _Framework.SessionComponent import SessionComponent
 
from SessionControl import SessionControl
from MixerControl import MixerControl
from DeviceControl import DeviceControl
from TrackControl import TrackControl
 
#from TimerComponent import TimerComponent
 
 
class PocketDial(ControlSurface):
    __module__ = __name__
    __doc__ = "PocketDial MIDI Remote Script"
    #session = None
     
    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        #self.log_message(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------= PocketDial log opened =--------------")
 
        # turn off rebuild MIDI map until after setup
        self.set_suppress_rebuild_requests(True)
         
        self._controls = [EncoderElement(MIDI_CC_TYPE, settings.CHANNEL, cc, settings.MAP_MODE) for cc in settings.CCS]
 
        mixer = MixerControl(self)
        session = SessionControl(self)
 
        device = DeviceControl(self)
        track = TrackControl(self)
 
        #timer = TimerComponent(self)
#       def _translate_message(self, type, from_identifier, from_channel, to_identifier, to_channel):
#       if not type in (MIDI_CC_TYPE, MIDI_NOTE_TYPE):
#           raise AssertionError
#           raise from_identifier in range(128) or AssertionError
#           raise from_channel in range(16) or AssertionError
#           raise to_identifier in range(128) or AssertionError
#           raise to_channel in range(16) or AssertionError
#           type == MIDI_CC_TYPE and self._c_instance.set_cc_translation(from_identifier, from_channel, to_identifier, to_channel)
#       elif type == MIDI_NOTE_TYPE:
#           self._c_instance.set_note_translation(from_identifier, from_channel, to_identifier, to_channel)
#       else:
#           raise False or AssertionError
         
 
 
        # Live 9 only
        #self.set_highlighting_session_component(session)
         
        # bind mixer to session
        session.component.set_mixer(mixer.component)
         
        # "magic" internal self._device_component, which enables lock to device, etc.
        self.set_device_component(device.component)
         
        # register components needed? works without
        #self._register_component(session.component)
        #self._register_component(mixer.component)
        #self._register_component(device.component)
         
     
        self._device = device
        self._track = track
 
        # turn rebuild back on
        self.set_suppress_rebuild_requests(False)
     
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
 
    def connect_script_instances(self, instanciated_scripts):
        for script in instanciated_scripts:
            if script == self:
                self.log_message("das bin ich selbst")
            else:
                self.log_message(script.__module__)
