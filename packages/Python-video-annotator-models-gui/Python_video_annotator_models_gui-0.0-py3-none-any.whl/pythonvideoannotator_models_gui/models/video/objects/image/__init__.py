from confapp import conf
from pythonvideoannotator_models_gui.models.video.objects.image.image_gui import ImageGUI

Image = type(
	'Image',
	tuple(conf.MODULES.find_class('models.video.objects.image.Image') + [ImageGUI]),
	{}
)
