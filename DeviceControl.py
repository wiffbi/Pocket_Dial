import settings
from _Framework.InputControlElement import *
from _Framework.EncoderElement import EncoderElement
from _Framework.DeviceComponent import DeviceComponent

class DeviceControl():
	def __init__(self, control_surface):
		self.control_surface = control_surface
		self.component = DeviceComponent()
		
		self._locked_device = None
		
		controls = []
		for cc in (96, 97, 98, 99, 104, 105, 106, 107):
			controls.append(EncoderElement(MIDI_CC_TYPE, \
										settings.CHANNEL, \
										cc, \
										Live.MidiMap.MapMode.relative_two_compliment))
		self.component.set_parameter_controls(tuple(controls))
		
		#self.component.set_lock_callback(self.device_locked)
		
		EncoderElement(	MIDI_CC_TYPE, \
						settings.CHANNEL, \
						110, \
						Live.MidiMap.MapMode.relative_two_compliment)\
			.add_value_listener(self.scroll_devices)

#		EncoderElement(	MIDI_CC_TYPE, \
#						settings.CHANNEL, \
#						100, \
#						Live.MidiMap.MapMode.relative_two_compliment)\
#			.add_value_listener(self._device_onoff)
	
	def lock_to_device(self, device):
		#self.control_surface.log_message("device_locked")
		self._locked_device = device
	
	def unlock_from_device(self, device):
		#self.control_surface.log_message("device_unlocked")
		self._locked_device = None
	
	
	def _device_onoff(self, value):
		# only react to left turns
		if value < 65:
			return
		
		if self._locked_device:
			device = self._locked_device
		else:
			device = self.control_surface.song().view.selected_track.view.selected_device
		
		if device:
			param = device.parameters[0]
			if param.value > 0:
				param.value = 0
			else:
				param.value = 1
	
	def _get_device_index(self, device, devices):
		index = 0
		for d in devices:
			if d == device:
				return index
			index = index + 1
		return -1

	def _get_device_recursive(self, selected_device, delta):
		if not selected_device:
			return None
		container = selected_device.canonical_parent # either track or chain
		if not container:
			return None
		len_devices = len(container.devices)
		index = self._get_device_index(selected_device, container.devices) + delta

		if not type(container) == type(Live.Track.Track):
			# as we are not inside a Track, we must be inside a Rack
			if index < 0:
				# if first device is selected and we move left, try to move up a device_container and select the containing device
				return self._get_device_recursive(container.canonical_parent, index+1)
			elif index >= len_devices:
				# if last device is selected and we move right, try to move up a device_container and select next device
				#return self.get_device_relative_recursive(container.canonical_parent, index-len_devices+1)
				# if last device is selected and we move right, try to move up a device_container and select the containing device
				return self._get_device_recursive(container.canonical_parent, index-len_devices)

		# we cannot move further out => stay inside the index-boundary of available devices
		index = max(0, min(len_devices-1, index))

		return container.devices[index]

	def scroll_devices(self, value):
		if value > 65:
			value = value - 128
		view = self.control_surface.song().view
		device = self._get_device_recursive(view.selected_track.view.selected_device, value)
		if device and not device == view.selected_track.view.selected_device:
			view.select_device(device)
			self.component.set_device(device)
	
	