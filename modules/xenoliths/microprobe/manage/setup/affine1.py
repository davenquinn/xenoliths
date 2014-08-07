def transform_coordinates(self, seed_file):
    dtype = [("point", int), ("x", float), ("y", float)]
    try:
        affine_seed = N.loadtxt(seed_file, comments="#", dtype=dtype)
    except IOError:
        print "No affine seed points available for "+seed_file
        return self.records

    fromCoords = []
    toCoords = []
    for a in affine_seed:
        idx = self.records['Line Numbers'] == a['point']
        point = self.records[idx][0]
        cord = [point[i+" Stage Coordinates (mm)"] for i in ["X","Y"]]
        tocord = [a["x"], a["y"]]
        print u"{} -> {}".format(repr(cord),repr(tocord))
        fromCoords.append(cord)
        toCoords.append(tocord)

    affine = Affine.construct(fromCoords, toCoords, verbose=True)

    incoords = [self.records[i+" Stage Coordinates (mm)"] for i in ["X","Y"]]
    incoords = N.transpose(N.vstack(incoords))
    outcords = affine.transform(incoords)
    for i,a in enumerate(["X","Y"]):
        self.records[a+" Stage Coordinates (mm)"] = outcords[:,i]
