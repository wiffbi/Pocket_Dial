import Live # This allows us (and the Framework methods) to use the Live API on occasion
import time # We will be using time functions for time-stamping our log file outputs
import settings
from SessionControl import SessionControl
from MixerControl import MixerControl


""" All of the Framework files are listed below, but we are only using using some of them in this script (the rest are commented out) """
from _Framework.ButtonElement import ButtonElement # Class representing a button a the controller
#from _Framework.ButtonMatrixElement import ButtonMatrixElement # Class representing a 2-dimensional set of buttons
#from _Framework.ButtonSliderElement import ButtonSliderElement # Class representing a set of buttons used as a slider
from _Framework.ChannelStripComponent import ChannelStripComponent # Class attaching to the mixer of a given track
#from _Framework.ChannelTranslationSelector import ChannelTranslationSelector # Class switches modes by translating the given controls' message channel
from _Framework.ClipSlotComponent import ClipSlotComponent # Class representing a ClipSlot within Live
from _Framework.CompoundComponent import CompoundComponent # Base class for classes encompasing other components to form complex components
from _Framework.ControlElement import ControlElement # Base class for all classes representing control elements on a controller
from _Framework.ControlSurface import ControlSurface # Central base class for scripts based on the new Framework
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent # Base class for all classes encapsulating functions in Live
#from _Framework.DeviceComponent import DeviceComponent # Class representing a device in Live
#from _Framework.DisplayDataSource import DisplayDataSource # Data object that is fed with a specific string and notifies its observers
from _Framework.EncoderElement import EncoderElement # Class representing a continuous control on the controller

from _Framework.InputControlElement import * # Base class for all classes representing control elements on a controller
#from _Framework.LogicalDisplaySegment import LogicalDisplaySegment # Class representing a specific segment of a display on the controller
from _Framework.MixerComponent import MixerComponent # Class encompassing several channel strips to form a mixer
#from _Framework.ModeSelectorComponent import ModeSelectorComponent # Class for switching between modes, handle several functions with few controls
#from _Framework.NotifyingControlElement import NotifyingControlElement # Class representing control elements that can send values
#from _Framework.PhysicalDisplayElement import PhysicalDisplayElement # Class representing a display on the controller
from _Framework.SceneComponent import SceneComponent # Class representing a scene in Live
from _Framework.SessionComponent import SessionComponent # Class encompassing several scene to cover a defined section of Live's session
from _Framework.SessionZoomingComponent import SessionZoomingComponent # Class using a matrix of buttons to choose blocks of clips in the session
from _Framework.SliderElement import SliderElement # Class representing a slider on the controller
#from _Framework.TrackEQComponent import TrackEQComponent # Class representing a track's EQ, it attaches to the last EQ device in the track
#from _Framework.TrackFilterComponent import TrackFilterComponent # Class representing a track's filter, attaches to the last filter in the track
from _Framework.TransportComponent import TransportComponent # Class encapsulating all functions in Live's transport section

""" Here we define some global variables """

class PocketDial(ControlSurface):
	__module__ = __name__
	__doc__ = " PocketDial MIDI Remote Script"
	
	def __init__(self, c_instance):
		"""everything except the '_on_selected_track_changed' override and 'disconnect' runs from here"""
		ControlSurface.__init__(self, c_instance)
		#self.log_message(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------= PocketDial log opened =--------------")
		
		# turn off rebuild MIDI map until after setup
		#self.set_suppress_rebuild_requests(True)
		
		
		#self._setup_transport_control() # Run the transport setup part of the script
		#self._setup_mixer_control() # Setup the mixer object
		#self._session = None
		#self._setup_session_control()  # Setup the session object	   
		
		
		session = SessionControl(self)
		mixer = MixerControl(self)
		
		# bind mixer to session
		session.component.set_mixer(mixer.component)
		
		#self.components.append(session.component)
		#self.components.append(mixer.component)
		
		self._session = session
		
		""" Here is some Live API stuff just for fun """
		app = Live.Application.get_application() # get a handle to the App
		maj = app.get_major_version() # get the major version from the App
		min = app.get_minor_version() # get the minor version from the App
		bug = app.get_bugfix_version() # get the bugfix version from the App
		self.show_message(str(maj) + "." + str(min) + "." + str(bug)) #put them together and use the ControlSurface show_message method to output version info to console
		
		#self.song().add_scenes_listener(self._set_scenecount)
		#self.song().add_tracks_listener(self._set_trackcount)
		#self._set_trackcount()
		#self._set_scenecount()
		
		# turn rebuild back on
		#self.set_suppress_rebuild_requests(False)
		

#	def _set_trackcount(self):
#		self.log_message("Tracks changed " + str(len(self.song().tracks)))
#		self.log_message("Return-Tracks changed " + str(len(self.song().return_tracks)))
#		self._trackcount = len(self.song().tracks)
#		self._returncount = len(self.song().return_tracks)
#	def _set_scenecount(self):
#		self.log_message("Scenes changed " + str(len(self.song().scenes)))
#		self._scenecount = len(self.song().scenes)
#		self.log_message("session.height = %d" % self._session.height())

#	def handle_sysex(self, midi_bytes):
#		pass


#	def _setup_transport_control(self):
#		is_momentary = True # We'll only be using momentary buttons here
#		transport = TransportComponent() #Instantiate a Transport Component
#		"""set up the buttons"""
#		transport.set_play_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 61)) #ButtonElement(is_momentary, msg_type, channel, identifier) Note that the MIDI_NOTE_TYPE constant is defined in the InputControlElement module
#		transport.set_stop_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 63))
#		transport.set_record_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 66))
#		transport.set_overdub_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 68))
#		transport.set_nudge_buttons(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 75), ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 73)) #(up_button, down_button)
#		transport.set_tap_tempo_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 78))
#		transport.set_metronome_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 80)) #For some reason, in Ver 7.x.x this method's name has no trailing "e" , and must be called as "set_metronom_button()"...
#		transport.set_loop_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 82))
#		transport.set_punch_buttons(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 85), ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 87)) #(in_button, out_button)
#		transport.set_seek_buttons(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 90), ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 92)) # (ffwd_button, rwd_button)
#		"""set up the sliders"""
#		transport.set_tempo_control(SliderElement(MIDI_CC_TYPE, CHANNEL, 26), SliderElement(MIDI_CC_TYPE, CHANNEL, 25)) #(control, fine_control)
#		transport.set_song_position_control(SliderElement(MIDI_CC_TYPE, CHANNEL, 24))

#	def _setup_mixer_control(self):
#		"""Here we set up the global mixer""" #Note that it is possible to have more than one mixer...
#		self._mixer = MixerComponent(6, 2, with_eqs=False, with_filters=False) #(num_tracks, num_returns, with_eqs, with_filters)
#		mixer = self._mixer
#		mixer.set_track_offset(0) #Sets start point for mixer strip (offset from left)
#		self.song().view.selected_track = mixer.channel_strip(0)._track #set the selected strip to the first track, so that we don't, for example, try to assign a button to arm the master track, which would cause an assertion error
#		"""set up the mixer buttons"""		
#		#mixer.set_select_buttons(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 56),ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 54)) #left, right track select	  
#		#mixer.master_strip().set_select_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 94)) #jump to the master track
#		#mixer.selected_strip().set_mute_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 42)) #sets the mute ("activate") button
#		#mixer.selected_strip().set_solo_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 44)) #sets the solo button
#		#mixer.selected_strip().set_arm_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 46)) #sets the record arm button
#		"""set up the mixer sliders"""
#		#mixer.selected_strip().set_volume_control(SliderElement(MIDI_CC_TYPE, CHANNEL, 14)) #sets the continuous controller for volume
#		"""note that we have split the mixer functions across two scripts, in order to have two session highlight boxes (one red, one yellow), so there are a few things which we are not doing here..."""
#		track_volume_ccs = [72, 73, 74, 75, 76, 77]
#		track_pan_ccs = [64, 65, 66, 67, 68, 69]
#		
#		track_send_a_ccs = [80, 81, 82, 83, 84, 85]
#		track_send_b_ccs = [88, 89, 90, 91, 92, 93]
#		for index in range(len(track_volume_ccs)):
# 			#mixer.channel_strip(index).set_select_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, track_select_notes[index]))
#			mixer.channel_strip(index).set_volume_control(EncoderElement(MIDI_CC_TYPE, 0, track_volume_ccs[index], Live.MidiMap.MapMode.relative_two_compliment))
#			mixer.channel_strip(index).set_pan_control(EncoderElement(MIDI_CC_TYPE, 0, track_pan_ccs[index], Live.MidiMap.MapMode.relative_two_compliment))
#			
#			mixer.channel_strip(index).set_send_controls((EncoderElement(MIDI_CC_TYPE, 0, track_send_a_ccs[index], Live.MidiMap.MapMode.relative_two_compliment), EncoderElement(MIDI_CC_TYPE, 0, track_send_b_ccs[index], Live.MidiMap.MapMode.relative_two_compliment)))
#		
#		
#		mixer.return_strip(0).set_volume_control(EncoderElement(MIDI_CC_TYPE, 0, 86, Live.MidiMap.MapMode.relative_two_compliment))
#		mixer.return_strip(1).set_volume_control(EncoderElement(MIDI_CC_TYPE, 0, 94, Live.MidiMap.MapMode.relative_two_compliment))
#	
#	
#		
#
#	def _track_nav(self, value, sender):
#		#self.log_message("PocketDial received " + str(value))
#		#self.log_message("PocketDial received by " + str(sender.message_map_mode()))
#		#self.show_message("PocketDial received " + str(value))
#		if value > 65:
#			value = value-128
#		
#		session = self._session
#		session.set_offsets(min(max(0, session.track_offset()+value), self._trackcount-6), session.scene_offset())
#	
#	def _scene_nav(self, value, sender):
#		if value > 65:
#			value = value-128
#		session = self._session
#		session.set_offsets(session.track_offset(), min(max(0, session.scene_offset()+value), self._scenecount-2))
#	
#	
#	def _trigger_clip(self, scene_index, track_index, value):
#		#self.log_message("PocketDial: trigger clip " + str(scene_index) +":" + str(track_index) + " => " + str(value))
#		#self.show_message("PocketDial: trigger clip " + str(scene_index) +":" + str(track_index) + " => " + str(value))
#		
#		session = self._session
#		track = self.song().tracks[session.track_offset()+track_index]
#		if value > 65:
#			track.stop_all_clips()
#		else:
#			track.clip_slots[session.scene_offset()+scene_index].fire()
#		
#	
#	def _setup_cc_launchpad(self, scene_index, track_index, encoder):
#		encoder.add_value_listener(lambda value: self._trigger_clip(scene_index, track_index, value))
#	
#	
#	
#	def _setup_session_control(self):
#		self._setup_mixer_control()
#		
#		
#		
#		self._session = SessionComponent(6, 2)
#		session = self._session
#		session.set_offsets(0, 0) #(track_offset, scene_offset) Sets the initial offset of the "red box" from top left
#		"""set up the session navigation"""
#		# track navigation
#		for cc in [79, 95, 111, 127]:
#			EncoderElement(MIDI_CC_TYPE, 0, cc, Live.MidiMap.MapMode.relative_two_compliment).add_value_listener(self._track_nav, True)
#		
#		# scene navigation
#		EncoderElement(MIDI_CC_TYPE, 0, 119, Live.MidiMap.MapMode.relative_two_compliment).add_value_listener(self._scene_nav, True)
#		
#		
#		
#		
#		# Launchpad from Scene 4
#		clip_launch_ccs = [(112, 113, 114, 115, 116, 117), (120, 121, 122, 123, 124, 125)]
#		for scene_index in range(len(clip_launch_ccs)):
#			for track_index in range(len(clip_launch_ccs[scene_index])):
#				self._setup_cc_launchpad(scene_index, track_index, EncoderElement(MIDI_CC_TYPE, 0, clip_launch_ccs[scene_index][track_index], Live.MidiMap.MapMode.relative_two_compliment))
#		
#		
#		
#		
#		
#		
#		is_momentary = True
#		#session.set_select_buttons(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 25), ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 27)) # (next_button, prev_button) Scene select buttons - up & down - we'll also use a second ControlComponent for this (yellow box)
#		session.set_scene_bank_buttons(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 51), ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 49)) # (up_button, down_button) This is to move the "red box" up or down (increment track up or down, not screen up or down, so they are inversed)
#		session.set_track_bank_buttons(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 56), ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 54)) # (right_button, left_button) This moves the "red box" selection set left & right. We'll put our track selection in Part B of the script, rather than here...
#		#session.set_stop_all_clips_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 70))
#		#session.selected_scene().set_launch_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 30))
#		"""Here we set up the scene launch assignments for the session"""		
#		#launch_notes = [60, 62, 64, 65, 67, 69, 71] #this is our set of seven "white" notes, starting at C4
#		#for index in range(num_scenes): #launch_button assignment must match number of scenes
#		#	session.scene(index).set_launch_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, launch_notes[index])) #step through the scenes (in the session) and assign corresponding note from the launch_notes array
#		"""Here we set up the track stop launch assignment(s) for the session""" #The following code is set up for a longer array (we only have one track, so it's over-complicated, but good for future adaptation)..
#		#stop_track_buttons = []
#		#for index in range(num_tracks):
#		#	stop_track_buttons.append(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 58 + index))   #this would need to be adjusted for a longer array (because we've already used the next note numbers elsewhere)
#		#session.set_stop_track_clip_buttons(tuple(stop_track_buttons)) #array size needs to match num_tracks		
#		"""Here we set up the clip launch assignments for the session"""
#		clip_launch_notes = [(40, 41, 42, 43), (36, 37, 38, 39)]
#		for scene_index in range(len(clip_launch_notes)):
#			for clip_index in range(len(clip_launch_notes[scene_index])):
#				session.scene(scene_index).clip_slot(clip_index).set_launch_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, clip_launch_notes[scene_index][clip_index])) #step through scenes and assign a note to first slot of each	   
#		
#		for scene_index in range(2):
#			for clip_index in range(4):
#				pass
#		#		session.scene(scene_index).clip_slot(clip_index).set_launch_button(EncoderElement(MIDI_CC_TYPE, 0, (scene_index*clip_index + clip_index), Live.MidiMap.MapMode.absolute))
#				#session.scene(scene_index).clip_slot(clip_index).set_launch_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, (scene_index*clip_index + clip_index + 1)))
#		
#		"""Here we set up a mixer and channel strip(s) which move with the session"""
#		session.set_mixer(self._mixer) #Bind the mixer to the session so that they move together
#		
##	def _on_selected_track_changed(self):
##		"""This is an override, to add special functionality (we want to move the session to the selected track, when it changes)
##		Note that it is sometimes necessary to reload Live (not just the script) when making changes to this function"""
##		ControlSurface._on_selected_track_changed(self) # This will run component.on_selected_track_changed() for all components
##		"""here we set the mixer and session to the selected track, when the selected track changes"""
##		selected_track = self.song().view.selected_track #this is how to get the currently selected track, using the Live API
##		#mixer.channel_strip(0).set_track(selected_track)
##		all_tracks = ((self.song().tracks + self.song().return_tracks) + (self.song().master_track,)) #this is from the MixerComponent's _next_track_value method
##		index = list(all_tracks).index(selected_track) #and so is this
##		session.set_offsets(index, session._scene_offset) #(track_offset, scene_offset); we leave scene_offset unchanged, but set track_offset to the selected track. This allows us to jump the red box to the selected track.
#		
#		#self.components.append(session)
#		
			   
	def disconnect(self):
		"""clean things up on disconnect"""
		self.log_message(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------= ProjectX log closed =--------------") #Create entry in log file
		ControlSurface.disconnect(self)
		self._session.disconnect()
		return None