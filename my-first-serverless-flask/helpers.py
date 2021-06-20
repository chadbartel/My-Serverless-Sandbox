"""API service helper functions."""

def generator(obj):
    """Generate items from an iterable"""
    try:
        for i in obj:
            yield i
    except Exception as e:
        print(f'Error encountered while generating from iterable: {e}')


def find_id(gen, id:int, key:str=None):
    """Find the `id` value in generator"""
    key = 'id' if key is None else key
    try:
        for i in gen:
            if i[key] == int(id):
                return i
    except Exception as e:
        print(f'Error encountered while looking for \'{key}\': {e}')
        return None
