import pyforms, cv2
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlBoundingSlider
from mcvapi.blobs.find_blobs import FindBlobs as Class


class FindBlobs(Class, BaseWidget):
	
	def __init__(self, **kwargs):
		BaseWidget.__init__(self, 'Find blobs')
		Class.__init__(self, **kwargs)

		try:
			self.layout().setContentsMargins(10, 5, 10, 5)
			self.setMinimumHeight(55)
		except:
			pass
		self._area_range = ControlBoundingSlider('Filter by area', default=[100,90000], mininum=0, maximum=100000, horizontal=True)
		self._formset = ['_area_range']

		self._area_range.changed_event = self.__area_range_changed_event

	#####################################################################
	### EVENTS ##########################################################
	#####################################################################

	def __area_range_changed_event(self):
		self._param_findblobs_min_area, self._param_findblobs_max_area = self._area_range.value
	