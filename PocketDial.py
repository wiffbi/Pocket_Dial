import Live
import time # We will be using time functions for time-stamping our log file outputs
import settings
from _Framework.ControlSurface import ControlSurface
from SessionControl import SessionControl
from MixerControl import MixerControl
from GlobalControl import GlobalControl
from DeviceControl import DeviceControl
from TrackControl import TrackControl


class PocketDial(ControlSurface):
	__module__ = __name__
	__doc__ = " PocketDial MIDI Remote Script"
	
	def __init__(self, c_instance):
		ControlSurface.__init__(self, c_instance)
		#self.log_message(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------= PocketDial log opened =--------------")
		
		# turn off rebuild MIDI map until after setup
		self.set_suppress_rebuild_requests(True)
		
		session = SessionControl(self)
		mixer = MixerControl(self)
		device = DeviceControl(self)
		track = TrackControl(self)
		GlobalControl(self) # play/pause, undo/redo
		
		# bind mixer to session
		session.component.set_mixer(mixer.component)
		
		# "magic" internal self._device_component, which enables lock to device, etc.
		self.set_device_component(device.component)
		
		# register components
		self._register_component(session.component)
		self._register_component(mixer.component)
		self._register_component(device.component)
		
		
		self._device = device
		self._track = track
		
		""" Here is some Live API stuff just for fun """
		app = Live.Application.get_application() # get a handle to the App
		maj = app.get_major_version() # get the major version from the App
		min = app.get_minor_version() # get the minor version from the App
		bug = app.get_bugfix_version() # get the bugfix version from the App
		self.show_message(str(maj) + "." + str(min) + "." + str(bug)) #put them together and use the ControlSurface show_message method to output version info to console
		
		# turn rebuild back on
		self.set_suppress_rebuild_requests(False)
	
	
	def _on_selected_track_changed(self):
		#ControlSurface._on_selected_track_changed(self)
		self._track._on_selected_track_changed()
		
	
	def lock_to_device(self, device):
		ControlSurface.lock_to_device(self, device)
		self._device.lock_to_device(device)

	def unlock_from_device(self, device):
		ControlSurface.unlock_from_device(self, device)
		self._device.unlock_from_device(device)
	
#	def disconnect(self):
#		self.log_message(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------= PocketDial log closed =--------------") #Create entry in log file
#		ControlSurface.disconnect(self)
#		#self._session.disconnect()
#		return None