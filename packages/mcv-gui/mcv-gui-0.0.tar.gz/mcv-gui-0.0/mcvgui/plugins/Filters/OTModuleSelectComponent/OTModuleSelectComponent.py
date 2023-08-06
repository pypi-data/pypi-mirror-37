import mcvgui.core.utils.tools as tools

from mcvgui.core.modules.OTModulePlugin 		import OTModulePlugin
from mcvgui.core.modules.ModuleConnection  	import ModuleConnection
from datatypes.TypeComponentsVideoPipe  import TypeComponentsVideoPipe
from datatypes.TypeBWVideoPipe  		import TypeBWVideoPipe
from datatypes.TypeColorVideo 				import TypeColorVideo


from pyforms.controls 	import ControlPlayer
from pyforms.controls  	import ControlCombo
from pyforms.controls  	import ControlButton


class OTModuleSelectComponent(OTModulePlugin,TypeBWVideoPipe):
	

	def __init__(self, name):
		icon_path = tools.getFileInSameDirectory(__file__, 'iconsubbg.jpg')
		TypeBWVideoPipe.__init__(self)
		OTModulePlugin.__init__(self, name,  iconFile=icon_path)

		self._video 		 = ModuleConnection("Video", connecting=TypeComponentsVideoPipe)
		self._player 		 = ControlPlayer("Video player")
		self._colorComponent = ControlCombo("Component")
		
		self._colorComponent.addItem("A", 0)
		self._colorComponent.addItem("B", 1)
		self._colorComponent.addItem("C", 2)
		self._colorComponent.valueUpdated = self.refreshValue
		self._video.changed 		  	  = self.newVideoInputChoosen

		self._formset = [ 
				'_video',
				'_colorComponent',
				"_player",
			]
		
	def refreshValue(self, value): self._player.refresh()


	def newVideoInputChoosen(self):
		ModuleConnection.changed(self._video)
		value = self._video.value
		if value:
			self.open(value)
			self._player.value = self
			print value
			
	def read(self):
		res, imgs = self._video.value.read()
		return res, imgs[self._colorComponent.value]
