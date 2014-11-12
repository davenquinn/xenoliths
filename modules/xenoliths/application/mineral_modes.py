import numpy as N

def compute_modes(sample):
    arr = N.array(sample.classification)
    T = arr.size
	area = {}
	for m, item in minerals.items():
		mode = arr[arr == m].size/T
		if m == "na":
			na = mode
			continue
		area[m] = mode

	vol = {}
	for m, item in area.items():
		vol[m] = item**1.5
	total = sum(vol.itervalues())
	for m, item in vol.items():
		vol[m] = item/total

	wt = {}
	for m, item in vol.items():
		wt[m] = item*densities[m]
	total = sum(wt.itervalues())
	for m,item in wt.items():
		wt[m] = item/total

