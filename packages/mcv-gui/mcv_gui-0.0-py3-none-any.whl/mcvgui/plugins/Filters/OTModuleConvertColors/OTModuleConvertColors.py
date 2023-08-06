import mcvgui.core.utils.tools as tools, cv2

from mcvgui.core.modules.OTModulePlugin 		import OTModulePlugin
from mcvgui.core.modules.ModuleConnection  	import ModuleConnection
from datatypes.TypeComponentsVideoPipe  import TypeComponentsVideoPipe
from datatypes.TypeColorVideoPipe  			import TypeColorVideoPipe
from datatypes.TypeColorVideo 				import TypeColorVideo


from pyforms.controls 	import ControlPlayer
from pyforms.controls  	import ControlCombo
from pyforms.controls  	import ControlButton


class OTModuleConvertColors(OTModulePlugin,TypeColorVideoPipe):
	

	def __init__(self, name):
		icon_path = tools.getFileInSameDirectory(__file__, 'iconsubbg.jpg')
		TypeColorVideoPipe.__init__(self)
		OTModulePlugin.__init__(self, name,  iconFile=icon_path)

		self._video 		 = ModuleConnection("Video", connecting=TypeColorVideo)
		self._player 		 = ControlPlayer("Video player")
		self._colorDomain 	 = ControlCombo("Color domain")
		
		self._colorDomain.addItem("XYZ",    cv2.COLOR_BGR2XYZ)
		self._colorDomain.addItem("YCrCb",  cv2.COLOR_BGR2YCR_CB)
		self._colorDomain.addItem("HSV",    cv2.COLOR_BGR2HSV)
		self._colorDomain.addItem("HLS",    cv2.COLOR_BGR2HLS)
		self._colorDomain.addItem("Lab",    cv2.COLOR_BGR2LAB)
		self._colorDomain.addItem("Luv",    cv2.COLOR_BGR2LUV)

		self._colorDomain.changed = self._player.refresh
		self._video.changed 	  = self.newVideoInputChoosen
		self._player.processFrame = self.processFrame

		self._formset = [ 
				'_video',
				'_colorDomain',
				"_player",
			]
	
	def newVideoInputChoosen(self):
		ModuleConnection.changed(self._video)
		value = self._video.value
		if value:
			self.open(value)
			self._player.value = value
			
	def processFrame(self, frame):
		
		return cv2.cvtColor(frame, self._colorDomain.value)
