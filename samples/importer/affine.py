"""
Module with tools to solve coefficients of an affine transformation from sets of known locations.
Useful, for example, in fitting two cartesian coordinate systems together.

|x_1 y_1 1| |a d|   |x'_1 y'_1|
|x_2 y_2 1| |b e| = |x'_2 y'_2|
|x_3 y_3 1| |c f|   |x'_3 y'_3|
"""
import numpy as N


def augment(a):
	arr = N.ones((a.shape[0],a.shape[1]+1))
	arr[:,:-1] = a
	return arr

class Affine(object):
	def __init__(self, array=None):
		self.array = array

	def transform(self, points):
		return N.dot(augment(N.array(points)), self.array)

	@classmethod
	def construct(cls, fromCoordinates, toCoordinates, verbose=False):
		fromCoords = augment(N.array(fromCoordinates))
		toCoords = N.array(toCoordinates)
		model, residuals, rank, sv = N.linalg.lstsq(fromCoords, toCoords)
		if verbose:
			print model
		affine =  cls(model)

		sol = N.dot(fromCoords,affine.array)
		res = (toCoords - sol)
		if verbose:
			print "Pixel errors:"
			print res

		return affine


if __name__ == "__main__":
	import IPython

	IPython.embed()