import pyforms, cv2
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlFile
from mcvapi.masks.mask import Mask as Class


class Mask(Class, BaseWidget):
    
    def __init__(self, **kwargs):
        BaseWidget.__init__(self, 'Mask')
        Class.__init__(self, **kwargs)

        try:
            self.layout().setContentsMargins(10, 5, 10, 5)
            self.setMinimumHeight(100)
        except:
            pass

        self._maskimg = ControlFile('Mask image')
        self._formset = ['_maskimg']

        self._maskimg.changed_event = self.__maskimg_changed_event

        self._param_mask_img = None

    def __maskimg_changed_event(self):
        try:
            img = cv2.imread(self._maskimg.value)
            if len(img.shape)>2: img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            self._param_mask_img = img
        except:
            pass


if __name__ == '__main__': 
    pyforms.startApp(Mask)