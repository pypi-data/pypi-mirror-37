import numpy as np

from .base import BaseMixin
from . import utils


class BasePartMixin(BaseMixin):

	def get_example(self, i):
		res = super(BasePartMixin, self).get_example(i)
		if len(res) == 2:
			# result has only image and label
			im, lab = res
			parts = None
		else:
			# result has already parts
			im, parts, lab = res

		return im, parts, lab

class BBCropMixin(BasePartMixin):

	def __init__(self, crop_to_bb=False, crop_uniform=False, *args, **kwargs):
		super(BBCropMixin, self).__init__(*args, **kwargs)
		self.crop_to_bb = crop_to_bb
		self.crop_uniform = crop_uniform

	def bounding_box(self, i):
		bbox = self._get("bounding_box", i)
		x,y,w,h = [bbox[attr] for attr in "xywh"]
		if self.crop_uniform:
			x0 = x + w//2
			y0 = y + h//2

			crop_size = max(w//2, h//2)

			x,y = max(x0 - crop_size, 0), max(y0 - crop_size, 0)
			w = h = crop_size * 2
		return x,y,w,h

	def get_example(self, i):
		im, parts, label = super(BBCropMixin, self).get_example(i)
		if self.crop_to_bb:
			x,y,w,h = self.bounding_box(i)
			im = im[y:y+h, x:x+w]
			if parts is not None:
				parts[:, 1] -= x
				parts[:, 2] -= y
		return im, parts, label

class PartCropMixin(BasePartMixin):
	def __init__(self, return_part_crops=False, *args, **kwargs):
		super(PartCropMixin, self).__init__(*args, **kwargs)
		self.return_part_crops = return_part_crops

	def get_example(self, i):
		im, parts, label = super(PartCropMixin, self).get_example(i)
		assert hasattr(self, "ratio"), "\"ratio\" attribute is missing!"
		if not self.return_part_crops or parts is None or not hasattr(self, "ratio"):
			return im, label

		crops = utils.visible_crops(im, parts)
		idxs, _ = utils.visible_part_locs(parts)

		return crops[idxs], label


class PartRevealMixin(BasePartMixin):
	def __init__(self, reveal_visible=False, *args, **kwargs):
		super(PartRevealMixin, self).__init__(*args, **kwargs)
		self.reveal_visible = reveal_visible

	def get_example(self, i):
		im, parts, label = super(PartRevealMixin, self).get_example(i)
		assert hasattr(self, "ratio"), "\"ratio\" attribute is missing!"
		if not self.reveal_visible or parts is None or not hasattr(self, "ratio"):
			return im, label

		_, xy = utils.visible_part_locs(parts)
		im = utils.reveal_parts(im, xy, ratio=self.ratio)
		return im, lab


class UniformPartMixin(BasePartMixin):

	def __init__(self, uniform_parts=False, ratio=utils.DEFAULT_RATIO, *args, **kwargs):
		super(UniformPartMixin, self).__init__(*args, **kwargs)
		self.uniform_parts = uniform_parts
		self.ratio = ratio

	def get_example(self, i):
		im, parts, label = super(UniformPartMixin, self).get_example(i)
		if self.uniform_parts:
			parts = utils.uniform_parts(im, ratio=self.ratio)
		return im, parts, label

class RandomBlackOutMixin(BasePartMixin):

	def __init__(self, seed=None, rnd_select=False, n_parts=None, *args, **kwargs):
		super(RandomBlackOutMixin, self).__init__(*args, **kwargs)
		self.rnd = np.random.RandomState(seed)
		self.rnd_select = rnd_select
		self.n_parts = n_parts

	def get_example(self, i):
		im, parts, lab = super(RandomBlackOutMixin, self).get_example(i)
		if self.rnd_select:
			idxs, xy = utils.visible_part_locs(parts)
			rnd_idxs = utils.random_idxs(idxs, rnd=self.rnd, n_parts=self.n_parts)

			parts[:, -1] = 0
			parts[rnd_idxs, -1] = 1

		return im, parts, lab



# some shortcuts

class PartMixin(RandomBlackOutMixin, UniformPartMixin, BBCropMixin):
	"""
		TODO!
	"""

class RevealedPartMixin(PartRevealMixin, PartMixin):
	"""
		TODO!
	"""


class CroppedPartMixin(PartCropMixin, PartMixin):
	"""
		TODO!
	"""
