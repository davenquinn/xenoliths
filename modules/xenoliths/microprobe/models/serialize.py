from geoalchemy2.shape import to_shape, from_shape
from shapely.geometry import mapping
from math import isnan

def serialize(obj):
    """Makes geojson for the measurements"""
    oxides = {i._oxide:i.weight_percent for i in obj.data}
    oxides["Total"] = obj.oxide_total

    molar = {i._oxide:i.molar_percent for i in obj.data}

    # Deal with Cr-number when not everything has
    # chromium content
    cr_number = obj.cr_number
    try:
        nan = isnan(cr_number)
    except TypeError:
        nan = True
    if nan: cr_number = None

    return dict(
        type = "Feature",
        properties = dict(
            mineral = obj.mineral,
            sample = obj.sample_id,
            systems = obj.transforms,
            oxides = oxides,
            formula = obj.formula,
            molar = molar,
            id = obj.n,
            mg_number = obj.mg_number,
            cr_number = cr_number,
            tags = [tag.name for tag in obj.tags]),
        geometry=mapping(to_shape(obj.geometry)),
        location=mapping(to_shape(obj.location)))
