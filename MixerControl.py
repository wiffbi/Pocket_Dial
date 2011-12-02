import settings
from _Framework.InputControlElement import *
from _Framework.MixerComponent import MixerComponent
from _Framework.EncoderElement import EncoderElement

class MixerControl():
	def __init__(self, control_surface):
		self.component = MixerComponent(6, 2, with_eqs=False, with_filters=False) #(num_tracks, num_returns, with_eqs, with_filters)
		mixer = self.component
		
		mixer.set_track_offset(0) #Sets start point for mixer strip (offset from left)
		#self.song().view.selected_track = mixer.channel_strip(0)._track #set the selected strip to the first track, so that we don't, for example, try to assign a button to arm the master track, which would cause an assertion error
		
		track_volume_ccs = range(72, 78) #[72, 73, 74, 75, 76, 77]
		track_pan_ccs = range(64, 70) #[64, 65, 66, 67, 68, 69]
		
		track_send_a_ccs = range(88, 94) #[88, 89, 90, 91, 92, 93]
		track_send_b_ccs = range(80, 86) #[80, 81, 82, 83, 84, 85]
		for index in range(len(track_volume_ccs)):
			mixer.channel_strip(index).set_volume_control(EncoderElement(MIDI_CC_TYPE, settings.CHANNEL, track_volume_ccs[index], Live.MidiMap.MapMode.relative_two_compliment))
			mixer.channel_strip(index).set_pan_control(EncoderElement(MIDI_CC_TYPE, settings.CHANNEL, track_pan_ccs[index], Live.MidiMap.MapMode.relative_two_compliment))
			
			mixer.channel_strip(index).set_send_controls((EncoderElement(MIDI_CC_TYPE, settings.CHANNEL, track_send_a_ccs[index], Live.MidiMap.MapMode.relative_two_compliment), EncoderElement(MIDI_CC_TYPE, settings.CHANNEL, track_send_b_ccs[index], Live.MidiMap.MapMode.relative_two_compliment)))
		
		
		#mixer.return_strip(0).set_volume_control(EncoderElement(MIDI_CC_TYPE, settings.CHANNEL, 86, Live.MidiMap.MapMode.relative_two_compliment))
		#mixer.return_strip(1).set_volume_control(EncoderElement(MIDI_CC_TYPE, settings.CHANNEL, 94, Live.MidiMap.MapMode.relative_two_compliment))
		