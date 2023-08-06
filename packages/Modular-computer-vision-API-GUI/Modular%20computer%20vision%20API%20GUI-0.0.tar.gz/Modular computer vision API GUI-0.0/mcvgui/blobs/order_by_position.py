from pyforms.basewidget import BaseWidget
from mcvapi.blobs.order_by_position import OrderByPosition as Class

class OrderByPosition(Class, BaseWidget):
	
	def __init__(self, **kwargs):
		BaseWidget.__init__(self, 'Order by position')
		Class.__init__(self, **kwargs)

		try:
			self.layout().setContentsMargins(10, 5, 10, 5)
			self.setMinimumHeight(65)
		except:
			pass

		self.formset = ['info:Order the blobs by their last position.']