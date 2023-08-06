from pyforms.controls import ControlText
from pythonvideoannotator_models_gui.dialogs import Dialog

class IModelGUI(object):

	def __init__(self):
		self._name = ControlText('Name')
		self._name.changed_event = self.name_changed_event

	def __add__(self, obj):
		super(IModelGUI,self).__add__(obj)
		for dialog in Dialog.instantiated_dialogs: dialog += obj
		return self

	def __sub__(self, obj):
		super(IModelGUI,self).__sub__(obj)
		for dialog in Dialog.instantiated_dialogs: dialog -= obj
		return self


	def name_changed_event(self):
		if not hasattr(self, '_name_change_activated'): 
			self._name_changed_activated = True
			self.name = self._name.value
			del self._name_changed_activated


	@property
	def name(self): return self._name.value
	@name.setter
	def name(self, value):
		if not hasattr(self, '_name_changed_activated'): 
			self._name_change_activated = True
			self._name.value = value
			del self._name_change_activated

		if hasattr(self, 'treenode'): self.treenode.setText(0,value)

		for dialog in Dialog.instantiated_dialogs:  dialog.refresh()