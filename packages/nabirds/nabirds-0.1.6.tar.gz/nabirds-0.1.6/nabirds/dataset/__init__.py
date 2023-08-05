from .reading import AnnotationsReadMixin, ImageListReadingMixin
from .parts import PartMixin, RevealedPartMixin, CroppedPartMixin

class Dataset(PartMixin, AnnotationsReadMixin):
	"""
		TODO!
	"""
