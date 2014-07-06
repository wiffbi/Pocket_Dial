#import settings
#from _Framework.InputControlElement import *
from _Framework.MixerComponent import MixerComponent
#from _Framework.EncoderElement import EncoderElement

class MixerControl():
	def __init__(self, control_surface):
		self.song = control_surface.song
		self.component = MixerComponent(8, 4, with_eqs=False, with_filters=False) #(num_tracks, num_returns, with_eqs, with_filters)

		mixer = self.component
		mixer.set_track_offset(0) #Sets start point for mixer strip (offset from left)
		#self.song().view.selected_track = mixer.channel_strip(0)._track #set the selected strip to the first track, so that we don't, for example, try to assign a button to arm the master track, which would cause an assertion error

		for i in range(8):
			# top row for pan, lower row for volume
			mixer.channel_strip(i).set_pan_control(control_surface.get_encoder(0,i))
			mixer.channel_strip(i).set_volume_control(control_surface.get_encoder(0,i+8))

			# setup sends
			mixer.channel_strip(i).set_send_controls((control_surface.get_encoder(1,i), control_surface.get_encoder(1,i+8), control_surface.get_encoder(2,i), control_surface.get_encoder(2,i+8)))
		
		# Crossfader binden?
		#mixer.set_crossfader_control(control_surface.get_encoder(3,7))

		#mixer.return_strip(0).set_volume_control(EncoderElement(MIDI_CC_TYPE, settings.CHANNEL, 86, Live.MidiMap.MapMode.relative_two_compliment))
		#mixer.return_strip(1).set_volume_control(EncoderElement(MIDI_CC_TYPE, settings.CHANNEL, 94, Live.MidiMap.MapMode.relative_two_compliment))

#		#crossfader = SliderElement(MIDI_CC_TYPE, 0, 15)
#		#mixer.set_crossfader_control(crossfader)
#		for cc in (70, 86, 102):
#			encoder = EncoderElement(	MIDI_CC_TYPE, \
#										settings.CHANNEL, \
#										cc, \
#										Live.MidiMap.MapMode.relative_two_compliment)
#			encoder.add_value_listener(self._crossfader)
#
#	def _crossfader(self, value):
#		param = self.song().master_track.mixer_device.crossfader
#		if value > 65:
#			# translate rel2comp to relative (ie. negative) value
#			value-= 128
#		param.value = max(param.min, min(param.max, param.value + (value/100.0)))
