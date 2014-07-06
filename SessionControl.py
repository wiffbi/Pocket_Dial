from _Framework.SessionComponent import SessionComponent

class SessionControl():
	def __init__(self, control_surface):
		self.control_surface = control_surface
		self.width = 8
		self.height = 1
		
		self.component = SessionComponent(self.width, self.height)
		self.component.set_offsets(0, 0) #(track_offset, scene_offset) Sets the initial offset of the "red box" from top left

		# navigation
		control_surface.get_encoder(3,7).add_value_listener(self._track_nav)
		

	def _track_nav(self, value):
		value-= 64

		session = self.component
		track_offset = min(max(0, session.track_offset()+value), max(0, len(self.control_surface.song().tracks)-self.width))
		#self.control_surface.log_message("track_offset %d" % track_offset)
		session.set_offsets(track_offset, session.scene_offset())
