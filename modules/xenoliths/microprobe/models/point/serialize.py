from geoalchemy2.shape import to_shape, from_shape
from shapely.geometry import mapping

def serialize(obj):
    """Makes geojson for the measurements"""
    return dict(
        type = "Feature",
        properties = dict(
            mineral = obj.mineral.id,
            sample = obj.sample.id,
            systems = obj.transforms,
            oxides = obj.oxides,
            formula = obj.formula,
            molar = obj.molar,
            id = obj.n,
            params = obj.params,
            tags = [str(tag) for tag in obj.tags]),
        geometry=mapping(to_shape(obj.geometry)))
