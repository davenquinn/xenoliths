import operator

def compute_mineral(point):
	"""Mineral totals from Taylor 1998, adjusted to be slightly more forgiving"""

	t = point.transforms["minerals"]
	mineral = max(t.iteritems(), key=operator.itemgetter(1))[0]

	if mineral in ["ol","sp"]:
		ofu = 4
	else:
		ofu = 6

	point.formula = point.compute_formula(ofu)

	cation_total = point.formula["Total"]-ofu
	if mineral == "ol":
		if not 2.98 < cation_total < 3.02:
			mineral = "na"
		if not 0.98 < point.formula["Si"] < 1.02:
			mineral = "na"

	if mineral in ["opx", "cpx"]:
		if not 3.97 < cation_total < 4.03:
			mineral = "na"

	point.mineral = mineral

def data_quality(point, save=True):
	compute_mineral(point)

	if point.oxides["Total"] < 90:
		point.tags.add("bad")
	if save:
		point.save()
