import settings
from _Framework.InputControlElement import *
from _Framework.SessionComponent import SessionComponent
from _Framework.EncoderElement import EncoderElement

class SessionControl():
	def __init__(self, control_surface):
		self.control_surface = control_surface
		self.song = control_surface.song
		self.component = SessionComponent(6, 2)
		
		session = self.component
		session.set_offsets(0, 0) #(track_offset, scene_offset) Sets the initial offset of the "red box" from top left
		
		#self.song().add_scenes_listener(self._set_scenecount)
		#self.song().add_tracks_listener(self._set_trackcount)
		#self._set_trackcount()
		#self._set_scenecount()
		
		# track navigation
		for cc in [79, 95, 111, 127]:
			EncoderElement(	MIDI_CC_TYPE, \
							settings.CHANNEL, \
							cc, \
							Live.MidiMap.MapMode.relative_two_compliment)\
				.add_value_listener(self._track_nav, True)
		
		# scene navigation
		EncoderElement(	MIDI_CC_TYPE, \
						settings.CHANNEL, \
						119, \
						Live.MidiMap.MapMode.relative_two_compliment)\
			.add_value_listener(self._scene_nav, True)
		
		
		
		
		# Launchpad from Scene 4
		clip_launch_ccs = ((112, 113, 114, 115, 116, 117), (120, 121, 122, 123, 124, 125))
		for scene_index in range(len(clip_launch_ccs)):
			for track_index in range(len(clip_launch_ccs[scene_index])):
				self._setup_cc_launchpad(	scene_index, \
											track_index, \
											EncoderElement(	MIDI_CC_TYPE, \
															settings.CHANNEL, \
															clip_launch_ccs[scene_index][track_index], \
															Live.MidiMap.MapMode.relative_two_compliment))
		
		scene_launch_ccs = (118, 126)
		for scene_index in range(len(scene_launch_ccs)):
			self._setup_cc_scenelaunch(	scene_index, \
										EncoderElement(	MIDI_CC_TYPE, \
														settings.CHANNEL, \
														scene_launch_ccs[scene_index], \
														Live.MidiMap.MapMode.relative_two_compliment))
		
		
			
		
		
	
#	def _set_trackcount(self):
#		#self.log_message("Tracks changed " + str(len(self.song().tracks)))
#		#self.log_message("Return-Tracks changed " + str(len(self.song().return_tracks)))
#		self._trackcount = len(self.song().tracks)
#		self._returncount = len(self.song().return_tracks)
#	def _set_scenecount(self):
#		#self.log_message("Scenes changed " + str(len(self.song().scenes)))
#		self._scenecount = len(self.song().scenes)
#		#self.log_message("session.height = %d" % self._session.height())
	
	
	def _setup_cc_scenelaunch(self, scene_index, encoder):
		encoder.add_value_listener(lambda value: self._trigger_scene(scene_index, value))
	
	def _trigger_scene(self, scene_index, value):
		session = self.component
		offset = session.scene_offset()+scene_index
		scenes = self.song().scenes
		if offset >= len(scenes):
			return
		scene = scenes[offset]
		if value > 65:
			self.song().stop_all_clips()
		else:
			scenes[offset].fire()
	
	
	def _setup_cc_launchpad(self, scene_index, track_index, encoder):
		encoder.add_value_listener(lambda value: self._trigger_clip(scene_index, track_index, value))
	
	def _trigger_clip(self, scene_index, track_index, value):
		#self.log_message("PocketDial: trigger clip " + str(scene_index) +":" + str(track_index) + " => " + str(value))
		#self.show_message("PocketDial: trigger clip " + str(scene_index) +":" + str(track_index) + " => " + str(value))
		
		session = self.component
		offset = session.track_offset()+track_index
		tracks = self.song().tracks
		if offset >= len(tracks):
			return
		track = tracks[offset]
		if value > 65:
			track.stop_all_clips()
		else:
			track.clip_slots[session.scene_offset()+scene_index].fire()
	
	def _track_nav(self, value, sender):
		#self.log_message("PocketDial received " + str(value))
		#self.log_message("PocketDial received by " + str(sender.message_map_mode()))
		#self.show_message("PocketDial received " + str(value))
		if value > 65:
			value = value-128

		session = self.component
		track_offset = min(max(0, session.track_offset()+value), max(0, len(self.song().tracks)-6))
		self.control_surface.log_message("track_offset %d" % track_offset)
		session.set_offsets(track_offset, session.scene_offset())

	def _scene_nav(self, value, sender):
		if value > 65:
			value = value-128
		session = self.component
		session.set_offsets(session.track_offset(), min(max(0, session.scene_offset()+value), len(self.song().scenes)-2))
	
	
	
	
	def disconnect(self):
		#self.song().remove_scenes_listener(self._set_scenecount)
		#self.song().remove_tracks_listener(self._set_trackcount)
		pass