import settings
from _Framework.InputControlElement import *
from _Framework.EncoderElement import EncoderElement
from _Framework.ChannelStripComponent import ChannelStripComponent

class TrackControl():
	def __init__(self, control_surface):
		self.control_surface = control_surface
		self.song = control_surface.song()
		
		self.component = ChannelStripComponent()
		self.component.set_track(self.song.view.selected_track)
		
		
		
		for cc, callback in ((100, self._arm), (108, self._mute_solo), (111, self._track_nav)):
			EncoderElement(	MIDI_CC_TYPE, \
							settings.CHANNEL, \
							cc, \
							Live.MidiMap.MapMode.relative_two_compliment)\
				.add_value_listener(callback)
				
		#for cc, callback in ((101, "set_pan_control"), (109, "set_volume_control")):
		self.component.set_pan_control(\
			EncoderElement(	MIDI_CC_TYPE, \
							settings.CHANNEL, \
							101, \
							Live.MidiMap.MapMode.relative_two_compliment))
		self.component.set_volume_control(\
			EncoderElement(	MIDI_CC_TYPE, \
							settings.CHANNEL, \
							109, \
							Live.MidiMap.MapMode.relative_two_compliment))
	
	
	def _on_selected_track_changed(self):
		if self.song.view.selected_track:
			self.component.set_track(self.song.view.selected_track)
	
	
	
	def _get_all_tracks(self, only_visible = False):
		if not only_visible:
			return self.song.tracks + self.song.return_tracks + (self.song.master_track, )
		tracks = []
		for track in self.song.tracks:
			if track.is_visible:
				tracks.append(track)
		for track in self.song.return_tracks:
			tracks.append(track)
		tracks.append(self.song.master_track)
		return tracks
	# helper function to go from one track to the other
	def _get_track_by_delta(self, track, d_value):
		tracks = self._get_all_tracks(only_visible = True)
		max_tracks = len(tracks)
		for i in range(max_tracks):
			if track == tracks[i]:
				return tracks[max((0, min(i+d_value, max_tracks-1)))]
	
	
	
	
	def _arm(self, value):
		track = self.song.view.selected_track
		if track.can_be_armed:
			if value > 65:
				track.arm = False
			else:
				track.arm = True
		
	def _mute_solo(self, value):
		track = self.song.view.selected_track
		if value > 65:
			if track.solo:
				track.solo = False
			else:
				track.mute = True
		else:
			if track.mute:
				track.mute = False
			else:
				track.solo = True
		
		
	def _track_nav(self, value):
		if value > 65:
			value = value-128
		self.song.view.selected_track = self._get_track_by_delta(self.song.view.selected_track, value)