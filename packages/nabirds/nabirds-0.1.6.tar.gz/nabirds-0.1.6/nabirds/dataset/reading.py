from imageio import imread
from os.path import join, isfile

from .base import BaseMixin

class AnnotationsReadMixin(BaseMixin):

	def __init__(self, uuids, annotations, mode="RGB"):
		super(AnnotationsReadMixin, self).__init__()
		self.uuids = uuids
		self._annot = annotations
		self.mode = mode

	def __len__(self):
		return len(self.uuids)

	def _get(self, method, i):
		return getattr(self._annot, method)(self.uuids[i])

	def get_example(self, i):
		res = super(AnnotationsReadMixin, self).get_example(i)
		# if the super class returns something, then the class inheritance is wrong
		assert res is None, "AnnotationsReadMixin should be the last class in the hierarchy!"

		methods = ["image", "parts", "label"]
		im_path, parts, label = [self._get(m, i) for m in methods]

		im = imread(im_path, pilmode=self.mode)

		return im, parts, label


class ImageListReadingMixin(BaseMixin):
	def __init__(self, pairs, root="."):
		super(ImageListReadingMixin, self).__init__()
		with open(pairs) as f:
			self._pairs = [line.strip().split() for line in f]

		assert all([len(pair) == 2 for pair in self._pairs]), \
			"Invalid format of the pairs file!"

		self._root = root

	def __len__(self):
		return len(self._pairs)

	def get_example(self, i):
		im_file, label = self._pairs[i]

		im_path = join(self._root, im_file)
		assert isfile(im_path), "Image \"{}\" does not exist!".format(im_path)
		im = imread(im_path, pilmode="RGB")

		return im, int(label)
