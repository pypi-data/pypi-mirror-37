from mcvgui.core.plugins.Geometry.base.OTBaseModuleGeometry import OTBaseModuleGeometry
from mcvgui.core.modules.formcontrols.OTControlBase import OTControlBase
from mcvgui.core.modules.formcontrols.OTParamButton import OTParamButton
from mcvgui.core.modules.formcontrols.OTParamSlider import OTParamSlider
from mcvgui.core.modules.formcontrols.OTParamPlayer import OTParamPlayer
from mcvgui.core.modules.formcontrols.OTParamToggle import OTParamToggle
from mcvgui.core.modules.formcontrols.OTParamList import OTParamList
from mcvgui.core.modules.formcontrols.OTParamVideoInput import OTParamVideoInput
from mcvgui.core.modules.formcontrols.OTParamModuleConnection import OTParamModuleConnection

from mcvgui.core.plugins.Geometry.OTModuleCircleCenter.OTModuleCircleCenter import OTModuleCircleCenter
from mcvgui.core.utils.tools import createCirclePoints
import mcvgui.core.utils.tools as tools
from FindCircle import FindCircle 

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import cv2
import numpy
import pickle

class OTModuleCircleRadius(OTBaseModuleGeometry):

    def __init__(self, name):
        icon_path = tools.getFileInSameDirectory(__file__, 'radius.png')
        OTBaseModuleGeometry.__init__(self,name, iconFile = icon_path)

        
        self._video  = OTParamVideoInput("Video")
        self._circlecenter  = OTParamModuleConnection("Circle center", connecting=OTModuleCircleCenter)
        self._player = OTParamPlayer("Video")
        self._run = OTParamButton("Run")
       
        self._formset = [ ('_video','_circlecenter','_run'), "_player", "=",'_polygons' ]

        self._video.valueUpdated = self.videoSelected
        self._run.value = self.__run
        
        self._radius = None
        self._player.processFrame = self.processFrame
        
 

    def processFrame(self, frame):
        if self._circlecenter.value.center!=None:
            cv2.circle(frame, self._circlecenter.value.center, 10, (0,255,255), -1)

            if self._radius!=None:
                cv2.circle(frame, self._circlecenter.value.center, self._radius, (0,255,0), 2)
                
        return frame


    def videoSelected(self, value): self._player.value = value

    def __run(self):
        if self._circlecenter.value.center!=None:
            center = self._circlecenter.value.center
            finder = FindCircle()
            polar_radius, cartasian_radius = finder.find_radius( self._player.currentFrame, center )
            self._radius = cartasian_radius

            points = createCirclePoints( center,cartasian_radius)
            if points:
                self._polygons += ["Poly_%d" % self._polygons.count, points]