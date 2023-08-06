import mcvgui.core.utils.tools as tools, cv2

from pyforms.controls   import ControlPlayer
from pyforms.controls   import ControlCombo
from pyforms.controls   import ControlSlider

from mcvgui.core.modules.ModuleConnection  import ModuleConnection
from datatypes.TypeSingleChannelImage        import TypeSingleChannelImage
from datatypes.TypeBWVideoPipe            import TypeBWVideoPipe
from mcvgui.core.modules.OTModulePlugin    import OTModulePlugin


class OTModuleColorRangeFilter(OTModulePlugin,TypeSingleChannelImage):
    

    def __init__(self, name):
        icon_path = tools.getFileInSameDirectory(__file__, 'iconsubbg.jpg')
        OTModulePlugin.__init__(self, name,  iconFile=icon_path)
        TypeSingleChannelImage.__init__(self)

        self._video     = ModuleConnection("Video", connecting=TypeBWVideoPipe)
        self._player    = ControlPlayer("Video player")

        self._min = ControlSlider("Min", default=1, minimum=0, maximum=255)
        self._max = ControlSlider("Max", default=255, minimum=0, maximum=255)
        
        self._formset = [ 
                '_video',
                "_player",
                '_min',
                '_max'
            ]
        
        self._player.processFrame   = self.processFrame
        self._video.changed         = self.newVideoInputChoosen
        self._min.changed           = self._player.refresh
        self._max.changed           = self._player.refresh

    def newVideoInputChoosen(self):
        value = self._video.value
        if value:
            self.open(value)
            self._player.value = value

    def processFrame(self, frame):
        filtered = cv2.inRange(frame, self._min.value, self._max.value)
        return filtered