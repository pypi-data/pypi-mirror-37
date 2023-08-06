from confapp import conf
from pythonvideoannotator_models_gui.models.video.objects.geometry.geometry_gui import GeometryGUI

Geometry = type(
	'Geometry',
	tuple(conf.MODULES.find_class('models.video.objects.geometry.Geometry') + [GeometryGUI]),
	{}
)
