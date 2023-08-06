from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlSlider
from pyforms.controls import ControlButton
from mcvapi.masks.path_mask import PathMask as Class


class PathMask(Class, BaseWidget):
	
	def __init__(self, **kwargs):
		BaseWidget.__init__(self, 'Path mask')
		Class.__init__(self, **kwargs)

		try:
			self.layout().setContentsMargins(10, 5, 10, 5)
			self.setMinimumHeight(105)
		except:
			pass

		self._control_pathmask_radius  		 = ControlSlider('Mask radius', default=30,  minimum=1, maximum=600)
		self._control_pathmask_sel_paths_btn = ControlButton('Select paths to filter')


		self._formset = [ 
			'info:This filter will apply circular masks around paths. For each input video only its paths will be used.',
			('_control_pathmask_sel_paths_btn', '_control_pathmask_radius')
		]

		self._control_pathmask_radius.changed_event = self.__control_pathmask_radius_changed_event

	#####################################################################
	### EVENTS ##########################################################
	#####################################################################

	def __control_pathmask_radius_changed_event(self):
		self._param_pathmask_radius = self._control_pathmask_radius.value
		

	@property 
	def pathmask_select_paths_event(self):
		self._control_pathmask_sel_paths_btn.value
	
	@pathmask_select_paths_event.setter
	def pathmask_select_paths_event(self, value):
		self._control_pathmask_sel_paths_btn.value = value
	
        