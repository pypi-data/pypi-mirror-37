from confapp import conf
from pythonvideoannotator_models_gui.models.project_gui import ProjectGUI

Project = type(
	'Project',
	tuple(conf.MODULES.find_class('models.Project') + [ProjectGUI]),
	{}
)
