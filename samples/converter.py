"""Converts between coordinate systems. These can be compositional or literally anything."""

class Converter(object):
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
			print "Errors:"
			print res

		return affine