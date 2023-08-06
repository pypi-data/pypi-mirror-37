import pyforms, cv2
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlSlider
from mcvapi.blobs.biggests_blobs import BiggestsBlobs as Class


class BiggestsBlobs(Class, BaseWidget):
	
	def __init__(self, **kwargs):
		BaseWidget.__init__(self, 'Biggests blobs')
		Class.__init__(self, **kwargs)

		try:
			self.layout().setContentsMargins(10, 5, 10, 5)
			self.setMinimumHeight(55)
		except:
			pass

		self._n_blobs = ControlSlider('Find n blobs', default=1, minimum=1, maximum=10)
		self._formset = ['_n_blobs']

		self._n_blobs.changed_event = self.__n_blobs_changed_evt

	#####################################################################
	### PROPERTIES ######################################################
	#####################################################################

	def __n_blobs_changed_evt(self):
		self._param_biggestsblobs_n = self._n_blobs.value