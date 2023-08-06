import pyforms, cv2
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlCombo
from pyforms.controls import ControlSlider
from mcvapi.filters.adaptative_threshold import AdaptativeThreshold as Class


class AdaptativeThreshold(Class, BaseWidget):
	
	def __init__(self, **kwargs):
		BaseWidget.__init__(self, 'Adaptative threshold')
		Class.__init__(self, **kwargs)


		try:
			self.layout().setContentsMargins(10, 5, 10, 5)
			self.setMinimumHeight(100)
		except:
			pass

		self._field_adaptive_threshold_method       = ControlCombo('Method')
		self._field_adaptive_threshold_type         = ControlCombo('Type')
		self._field_adaptive_threshold_block_size   = ControlSlider('Block size', default=self._param_adaptivethreshold_block_size, minimum=3, maximum=2999)
		self._field_adaptive_threshold_c            = ControlSlider('C', default=self._param_adaptivethreshold_c,  minimum=0, maximum=500)

		self._formset = [
			('_field_adaptive_threshold_method','_field_adaptive_threshold_type'),
			('_field_adaptive_threshold_block_size','_field_adaptive_threshold_c')
		]

		self._field_adaptive_threshold_method.add_item('ADAPTIVE_THRESH_MEAN_C', cv2.ADAPTIVE_THRESH_MEAN_C)
		self._field_adaptive_threshold_method.add_item('ADAPTIVE_THRESH_GAUSSIAN_C', cv2.ADAPTIVE_THRESH_GAUSSIAN_C)

		self._field_adaptive_threshold_type.add_item('THRESH_BINARY_INV', cv2.THRESH_BINARY_INV)
		self._field_adaptive_threshold_type.add_item('THRESH_BINARY', cv2.THRESH_BINARY)

		self._field_adaptive_threshold_method.value = self._param_adaptivethreshold_method
		self._field_adaptive_threshold_type.value = self._param_adaptivethreshold_type


		self._field_adaptive_threshold_method.changed_event = self.__adaptative_threshold_changed_evt
		self._field_adaptive_threshold_type.changed_event = self.__adaptative_threshold_changed_evt
		self._field_adaptive_threshold_block_size.changed_event = self.__adaptative_threshold_changed_evt
		self._field_adaptive_threshold_c.changed_event = self.__adaptative_threshold_changed_evt


	#####################################################################
	### PROPERTIES ######################################################
	#####################################################################

	def __adaptative_threshold_changed_evt(self):
		self._param_adaptivethreshold_method 		= self._field_adaptive_threshold_method.value
		self._param_adaptivethreshold_type 			= self._field_adaptive_threshold_type.value
		self._param_adaptivethreshold_block_size 	= self._field_adaptive_threshold_block_size.value
		self._param_adaptivethreshold_c 			= self._field_adaptive_threshold_c.value-255