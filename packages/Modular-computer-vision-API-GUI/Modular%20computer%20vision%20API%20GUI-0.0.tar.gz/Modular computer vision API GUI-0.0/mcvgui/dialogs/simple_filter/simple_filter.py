import pyforms, cv2
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlList
from pyforms.controls import ControlPlayer
from pyforms.controls import ControlText
from pyforms.controls import ControlCombo
from mcvapi.mcvbase import MCVBase

from confapp import conf


class SimpleFilter(MCVBase, BaseWidget):
    """
    It implements a dialog that allow the user to choose several combinations of
    filters and apply them to a video.
    The player allow the user to pre visualize the result.
    """


    def __init__(self, parent=None, video=None):
        BaseWidget.__init__(self, 'Simple workflow editor', parent_win=parent)
        self._parent = parent

        self._player        = ControlPlayer('Player')
        self._imgfilters    = ControlList('Image filters')
        self._imageflows    = ControlCombo('Image workflows')
        self._blobsflows    = ControlCombo('Blobs workflows')
        self._blobsfilters  = ControlList('Blobs filters')

        self.formset = [
            '_player',
            '=',
            [{
                'a:Image filter':['_imageflows','_imgfilters'],
                'b:Blobs filter':['_blobsflows','_blobsfilters']
            }]
        ]

        self.load_order = ['_imageflows', '_blobsflows','_imgfilters','_blobsfilters']

        self._imgfilters.select_entire_row      = True
        self._blobsfilters.select_entire_row    = True
        self._imageflows.changed_event          = self.__imageflows_changed_event
        self._blobsflows.changed_event          = self.__blobsflows_changed_event
        self._player.process_frame_event        = self.__process_frame
        
        self.video_capture = video

        self._pipelines = {}   # dictinary with all the available pipelines
        self._pipeline  = None # active pipeline class
    
    ###########################################################################
    ### IO FUNCTIONS ##########################################################
    ###########################################################################
    def save(self, data={}, **kwargs):
        for n, f in self._imgfilters.value:   f.save(data, **kwargs)
        for n, f in self._blobsfilters.value: f.save(data, **kwargs)
        return data

    def load(self, data, **kwargs):
        for n, f in self._imgfilters.value:   f.load(data, **kwargs)
        for n, f in self._blobsfilters.value: f.load(data, **kwargs)
        
    ###########################################################################
    ### FUNCTIONS #############################################################
    ###########################################################################
    
    def clear(self):
        """
        Reinit all the filters
        """
        for name, f in self._imgfilters.value:      data = f.clear()
        for name, f in self._blobsfilters.value:    data = f.clear()
        self.pipeline = None

    def processflow(self, data, **kwargs):
        """
        Apply the selected workflow of filters.
        """
        if self.pipeline is None:
            self.pipeline = self.build_workflow_instance()

        return self.pipeline.processflow(data, **kwargs)

    def end(self, data, **kwargs):
        """
        Apply the selected workflow of filters.
        """
        if self.pipeline is None:
            self.pipeline = self.build_workflow_instance()

        return self.pipeline.end(data, **kwargs)

    def pipeline_classes(self):
        classes_list =  [f.__class__ for title, f in self._imgfilters.value]
        classes_list += [f.__class__ for title, f in self._blobsfilters.value]
        classes_list.reverse()

        return classes_list

    def build_workflow_instance(self):
        # export the configured parameters
        data = {'load': True}
        for name, f in self._imgfilters.value: f.save(data)
        for name, f in self._blobsfilters.value: f.save(data)

        # create the workflow class and import the configured parameters
        classes_list =  self.pipeline_classes()
        instance = type('ProcessingPipeline', tuple(classes_list), {})(**data)
        return instance

    ###########################################################################
    ### INTERFACE FUNCTIONS ###################################################
    ###########################################################################

    def __load_default_blobsflows(self):
        self._blobsflows.add_item('Find blobs + track path', 2)
        self.__blobsflows_changed_event()


    def __imageflows_changed_event(self):
        # A new image worflow was selected

        workflow = []
        for title, flow_filter in self._pipelines.get(self._imageflows.value, []):
            workflow.append( (title, flow_filter() ) )
        self.image_filters = workflow

        self.pipeline = None

    def __blobsflows_changed_event(self):
        # A new blob workflow was selected

        workflow = []
        for title, flow_filter in self._pipelines.get(self._blobsflows.value, []):
            workflow.append( (title, flow_filter() ) )
        self.blobs_filters = workflow

        self.pipeline = None

    def __process_frame(self, frame):
        frame_index = self._player.video_index-1
    
        data = frame
        for name, f in self._imgfilters.value:
            data = f.process(data, frame_index=frame_index)
        thresh = data
        for name, f in self._blobsfilters.value:
            data = f.process(data, frame_index=frame_index)

        step = 16581375 / (len(data)+1)

        for i, blob in enumerate(data):
            if blob is not None:
                rgb_int = int(step*(i+1))
                blue    =  rgb_int & 255
                green   = (rgb_int >> 8) & 255
                red     = (rgb_int >> 16) & 255
                c = (blue, green, red)

                #blob.draw(frame, color=c)
                if blob.centroid:
                    cv2.putText(frame,str(i), blob.centroid, cv2.FONT_HERSHEY_SIMPLEX, 1, c)

        return frame, thresh
        

    def add_image_filters(self, filtername, pipeline):
        """
        Add an image filter
        """
        first_filters = self._imageflows.value==None
        self._imageflows.add_item(filtername)
        self._pipelines[filtername] = pipeline
        if first_filters: self.__imageflows_changed_event()

    def add_blobs_filters(self, filtername, pipeline):
        """
        Add a blob filter
        """
        first_filters = self._blobsflows.value==None
        self._blobsflows.add_item(filtername)
        self._pipelines[filtername] = pipeline
        if first_filters: self.__blobsflows_changed_event()


    ###########################################################################
    ### PROPERTIES ############################################################
    ###########################################################################

    @property
    def image_filters(self):
        """
        Set and retrieve the selected list of image filters
        """
        for name, f in self._imgfilters.value: yield f
    @image_filters.setter
    def image_filters(self, value): self._imgfilters.value = value


    @property
    def blobs_filters(self):
        """
        Set and retrieve the selected list of blobs filters
        """
        for name, f in self._blobsfilters.value: yield f
    @blobs_filters.setter
    def blobs_filters(self, value): self._blobsfilters.value = value
    
    
    @property
    def video_capture(self): 
        """
        Set and retrieve the video for previsualization.
        The value should be from type cv2.VideoCapture or a path to a video file.
        """
        return self._player.value
    @video_capture.setter
    def video_capture(self, value):
        self._player.value  = value
        for name, f in self._imgfilters.value:      f.video = value
        for name, f in self._blobsfilters.value:    f.video = value

    def show(self):
        super(SimpleFilter, self).show()
        self._blobsfilters.show()
        self._blobsfilters.resize_rows_contents()


if __name__ == '__main__': 
    pyforms.start_app(SimpleFilter)