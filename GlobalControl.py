import settings
from _Framework.InputControlElement import *
from _Framework.EncoderElement import EncoderElement

class GlobalControl():
	def __init__(self, control_surface):
		self.control_surface = control_surface
		self.song = control_surface.song
		self.view = control_surface.application().view #Live.Application.get_application().view
		
		self.is_paused = False
		
		for cc in (70, 86, 102):
			encoder = EncoderElement(	MIDI_CC_TYPE, \
										settings.CHANNEL, \
										cc, \
										Live.MidiMap.MapMode.relative_two_compliment)
			encoder.add_value_listener(self._undo_redo)
		
		
		for cc in (71, 87, 103):
			encoder = EncoderElement(	MIDI_CC_TYPE, \
										settings.CHANNEL, \
										cc, \
										Live.MidiMap.MapMode.relative_two_compliment)
			encoder.add_value_listener(self._play_pause_stop)
		
	
	
	def _undo_redo(self, value):
		song = self.song()
		if value > 65:
			if song.can_undo:
				song.undo()
		elif song.can_redo:
			self.song().redo()
	
	def _play_pause_stop(self, value):
		# depending on what is visible
		song = self.song()
		if self.view.is_view_visible("Arranger"):
			if value > 65:
				if song.is_playing:
					self.is_paused = True
					song.stop_playing()
				else:
					self.is_paused = False
			else:
				if self.is_paused:
					song.continue_playing()
				else:
					song.start_playing()
			
		else: # Session is visible
			scene = self.song().view.selected_scene
			if value > 65:
				scene = self._get_scene_by_delta(scene, value-128)
			else:
				scene = self._get_scene_by_delta(scene, value)
			scene.fire()
			self.song().view.selected_scene = scene
	
	
	# helper function to go from one scene to the other
	def _get_scene_by_delta(self, scene, d_value):
		scenes = self.song().scenes
		max_scenes = len(scenes)
		for i in range(max_scenes):
			if scene == scenes[i]:
				return scenes[max((0, min(i+d_value, max_scenes-1)))]
	
	
	
	
	
