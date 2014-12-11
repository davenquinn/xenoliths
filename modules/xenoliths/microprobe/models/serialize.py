from geoalchemy2.shape import to_shape, from_shape
from shapely.geometry import mapping

def serialize(obj):
    """Makes geojson for the measurements"""
    oxides = {i._oxide:i.weight_percent for i in obj.data}
    oxides["Total"] = obj.oxide_total

    molar = {i._oxide:i.molar_percent for i in obj.data}

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
            cr_number = obj.cr_number,
            tags = [tag.name for tag in obj.tags]),
        geometry=mapping(to_shape(obj.geometry)))
