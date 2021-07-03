"""API service helper functions."""

# Import libraries
import os
import json
import logging
from pathlib import Path
import datetime

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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


def binary_search(l:list, item):
    """Perform binary search on a homogenous list for an item and return it's 
    location.
    Args:
        l (list): the homogenous list to be searched
        item (): the item to look for in the list
    Returns:
        int: index location of item in list or `None`
    """
    low = 0
    high = len(l) - 1
    # Cut `l` in half until `item` is found
    while low <= high:
        mid = (low + high)
        guess = l[mid]
        if guess == item:
            # Item was found
            return mid
        if guess > item:
            # Guess is too high
            high = mid - 1
        else:
            # Guess is too low
            low = mid + 1
    return None


def get_criteria():
    # Set project root
    root = Path(__file__).parent.parent

    # Load all associated criteria
    criteria = {}
    criteria_path = root
    for root, _, files in os.walk(criteria_path):
        for file in files:
            # Skip all non-json documents:
            if '.json' not in file or 'criteria' not in file:
                logger.info(
                    'Helper has received a non-valid json document: %s.',
                    file,
                )
                continue
            # Load criteria and return
            with open(file) as f:
                criteria = json.load(f)
    return criteria


def default(o):
    """Default datetime formatter for json."""
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()