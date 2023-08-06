from pyforms.controls import ControlTreeView
from pyforms.controls import ControlTree
from PyQt4 import QtGui
from PyQt4.QtCore import QSize
import os, glob


class PluginsTree(ControlTree):

	def __init__(self):
		super(PluginsTree, self).__init__('List of plugins')
		self.setHeaderHidden(True)
		self.setIconSize( QSize(16, 16) )

		path = os.path.dirname(__file__)
		self.__add2Node( self.invisibleRootItem(), os.path.join(path, '..', '..' ,'plugins') )

	def __readPluginTXT(self, filename):
		f = open(filename, 'r')
		str2eval = "".join(f.readlines()).strip()
		config = eval(str2eval)
		f.close()
		return config

	def __add2Node(self, node, searchpath):
		searchstr 	= os.path.join(searchpath,'*','folder.txt')
		files 		= glob.glob(searchstr)

		for filename in files:
			path,_ = os.path.split(filename)
			config = self.__readPluginTXT(filename)

			treeItem = QtGui.QTreeWidgetItem()
			if 'name' in config: treeItem.setText(0, config['name'])
			if 'icon' in config: treeItem.setIcon(0,
					QtGui.QIcon( os.path.join(path, config['icon']) )
				)
			if 'class' in config:
				treeItem.pluginfile = path
				treeItem.pluginclass = config['class']
			node.addChild(treeItem)

			self.__add2Node(treeItem, path)