from app.library import functions

GRAB_UTILS = {
    'uuid4_str': functions.uuid4_str,
    'unique_str': functions.generate_unique_string,
    'timestamp': functions.get_timestamp,
}


def filter_json(items):
    if not items:
        return None

    result = {}

    for item in items:
        if item.get('is_active'):
            result[item['name']] = item['value']

    return result
