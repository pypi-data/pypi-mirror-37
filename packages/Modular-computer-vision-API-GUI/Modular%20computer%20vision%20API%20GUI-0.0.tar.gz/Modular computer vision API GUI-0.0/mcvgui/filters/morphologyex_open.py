import pyforms, cv2, numpy as np
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlCheckBox
from pyforms.controls import ControlSlider
#from mcvapi.filters.background_detector import BackgroundDetector as Class
from mcvapi.filters.morphologyex_open import MorphologyExOpen as Class

class MorphologyExOpen(Class, BaseWidget):
	
	def __init__(self, **kwargs):
		BaseWidget.__init__(self, 'MorphologyEx open')
		Class.__init__(self, **kwargs)

		self._use_morphologyexopen 				 = ControlCheckBox('Use MorphologyEx Open')
		self._field_morphologyexopen_kernel_size = ControlSlider('Kernel size', default=self._param_morphologyexopen_kernel_size,  minimum=3, maximum=51)



		try:
			self.layout().setContentsMargins(10, 5, 10, 5)
			self.setMinimumHeight(50)
		except:
			pass

		
		self._formset = [
			('_use_morphologyexopen','_field_morphologyexopen_kernel_size')
		]

		self._field_morphologyexopen_kernel_size.changed_event = self.__update_param_morphologyex_kernel_size


	#####################################################################
	### PROPERTIES ######################################################
	#####################################################################

	def __update_param_morphologyex_kernel_size(self):
		self._param_morphologyexopen_kernel_size = kernel_size = self._field_morphologyexopen_kernel_size.value 

		if (kernel_size % 2)==0: kernel_size += 1

		self._param_morphologyexopen_kernel = np.ones((kernel_size,kernel_size),np.uint8)
