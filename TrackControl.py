#import settings
from _Framework.ChannelStripComponent import ChannelStripComponent

class TrackControl():
	def __init__(self, control_surface):
		self.control_surface = control_surface
		self.song = control_surface.song()
		
		self.component = ChannelStripComponent()
		self.component.set_track(self.song.view.selected_track)

		self.component.set_volume_control(control_surface.get_encoder(3,12))
		self.component.set_pan_control(control_surface.get_encoder(3,4))
		self.component.set_send_controls((control_surface.get_encoder(3,5), control_surface.get_encoder(3,13), control_surface.get_encoder(3,6), control_surface.get_encoder(3,14)))

		# track navigation
		#control_surface.get_encoder(3,7).add_value_listener(self._track_nav)
	
	
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
	
		
	def _track_nav(self, value):
		value-= 64
		self.song.view.selected_track = self._get_track_by_delta(self.song.view.selected_track, value)
