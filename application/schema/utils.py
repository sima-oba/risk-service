import dataclasses


def export_feature_collection(objects: list, include_geometry=True):
    if len(objects) == 0:
        return {
            'type': 'FeatureCollection',
            'features': []
        }

    features = []

    for index, data in enumerate(objects):
        if dataclasses.is_dataclass(data):
            data = dataclasses.asdict(data)

        geometry = data.pop('geometry', None)
        properties = {key: value for key, value in data.items()}
        feature = {
            'id': index,
            'type': 'Feature',
            'properties': properties
        }

        if include_geometry:
            feature['geometry'] = geometry

        features.append(feature)

    return {
        'type': 'FeatureCollection',
        'features': features
    }
