import operator

def compute_mineral(point):
	t = point.transforms["minerals"]
	mineral = max(t.iteritems(), key=operator.itemgetter(1))[0]
	point.mineral = mineral

def data_quality(point):
	compute_mineral(point)

	if point.oxides["Total"] < 90:
		point.tags.add("bad")
	point.save()
