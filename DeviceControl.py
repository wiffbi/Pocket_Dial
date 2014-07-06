#import settings
import Live
from _Framework.DeviceComponent import DeviceComponent
from _Framework.InputControlElement import MIDI_CC_TYPE	
from _Framework.EncoderElement import EncoderElement

class DeviceControl():
	def __init__(self, control_surface):
		self.control_surface = control_surface
		self.component = DeviceComponent()
		
		self._locked_device = None
		
		# register left 4 encoders in two rows from bank 4 as parameter controls
		self.component.set_parameter_controls(tuple([control_surface.get_encoder(3,i) for i in (0,1,2,3,8,9,10,11)]))

		# device navigation
		control_surface.get_encoder(3,15).add_value_listener(self.scroll_devices)

	
	def lock_to_device(self, device):
		#self.control_surface.log_message("device_locked")
		self._locked_device = device
		#for i in dir(device):
		#	self.control_surface.log_message("%s" % i)
	
	def unlock_from_device(self, device):
		#self.control_surface.log_message("device_unlocked")
		self._locked_device = None
	
	


	def _get_all_tracks(self, only_visible = False):
		song = self.control_surface.song()
		tracks = []
		for track in song.tracks:
			if only_visible and track.is_visible:
				tracks.append(track)
			else:
				tracks.append(track)
		for track in song.return_tracks:
			tracks.append(track)
		tracks.append(song.master_track)
		return tracks

	# helper function to go from one track to the other
	def _get_track_by_delta(self, track, d_value):
		tracks = self._get_all_tracks(only_visible = True)
		max_tracks = len(tracks)
		for i in range(max_tracks):
			if track == tracks[i]:
				return tracks[max((0, min(i+d_value, max_tracks-1)))]


	def _get_device_index(self, device, devices):
		index = 0
		for d in devices:
			if d == device:
				return index
			index = index + 1
		return index

	def _get_device_recursive(self, track, device, delta):
		container = None
		if device:
			container = device.canonical_parent # either track or chain
		if not container:
			container = track
		
		len_devices = len(container.devices)
		if device:
			index = self._get_device_index(device, container.devices)
		elif delta >= 0:
			index = 0
		else:
			index = len(container.devices)
		index+= delta

		#self.control_surface.log_message("_get_device_recursive: delta: %d -> new index: %d" % (delta, index))

		if index < 0 or (index > 0 and index >= len_devices):
			# outside boundaries
			if hasattr(container, 'can_be_armed'):
				# we are on track level, so switch track
				if index < 0:
					prev_track = track
					track = self._get_track_by_delta(track, -1)
					if not track == prev_track:
						if len(track.devices):
							device = track.devices[len(track.devices)-1]
						else:
							device = None
						return self._get_device_recursive(track, device, index+1)
				else:
					prev_track = track
					track = self._get_track_by_delta(track, 1)
					if not track == prev_track:
						if len(track.devices):
							device = track.devices[0]
						else:
							device = None
						return self._get_device_recursive(track, device, index-max(1,len_devices))
					
			else:
				# we are inside a Chain
				if index < 0:
					# if first device is selected and we move left, try to move up a device_container and select the containing device
					return self._get_device_recursive(track, container.canonical_parent, index+1)
				elif index >= len_devices:
					# if last device is selected and we move right, try to move up a device_container and select next device
					#return self.get_device_relative_recursive(container.canonical_parent, index-len_devices+1)
					# if last device is selected and we move right, try to move up a device_container and select the containing device
					return self._get_device_recursive(track, container.canonical_parent, index-len_devices)



		# we cannot move further out => stay inside the index-boundary of available devices
		index = max(0, min(len_devices-1, index))
		if len(container.devices):
			return (track, container.devices[index])
		else:
			return (track, None)

	def scroll_devices(self, value):
		value-= 64 # relative_binary_offset auf signed int umrechnen
		view = self.control_surface.song().view
		track, device = self._get_device_recursive(view.selected_track, view.selected_track.view.selected_device, value)
		
		if not track == view.selected_track:
			view.selected_track = track
		if device:# and not device == view.selected_track.view.selected_device:
			view.select_device(device)
			self.component.set_device(device)
	
	
