import pyforms, cv2, numpy as np
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlCombo
from pyforms.controls import ControlSlider
#from mcvapi.filters.background_detector import BackgroundDetector as Class
from mcvapi.filters.background_subtract import BackgroundSubtract as Class

class BackgroundSubtract(Class, BaseWidget):
	
	def __init__(self, **kwargs):
		BaseWidget.__init__(self, 'Background subtract')
		Class.__init__(self, **kwargs)


		try:
			self.layout().setContentsMargins(10, 5, 10, 5)
			self.setMinimumHeight(100)
		except:
			pass

		self._field_background_subtract_threshold  = ControlSlider('Threshold', default=self._param_backgroundsubtract_threshold,  minimum=1, maximum=255)
		
		self._formset = [
			'_field_background_subtract_threshold',			
		]

		self._field_background_subtract_threshold.changed_event = self.__background_subtract_threshold_event

	#####################################################################
	### EVENTS ##########################################################
	#####################################################################

	def __background_subtract_threshold_event(self):
		self._param_backgroundsubtract_threshold = self._field_background_subtract_threshold.value
		
