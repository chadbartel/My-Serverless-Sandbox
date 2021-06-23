#!/usr/bin/env python

"""Simple Python class to wrap criteria file."""
# Import libraries
import os
import json
import logging
from copy import copy
from pathlib import Path

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Module classes
class Criteria:

    # Instance attributes
    @property
    def criteria(self) -> dict:
        """Return copy of read-only _criteria attribute."""
        return copy(self._criteria)

    def __init__(self):
        # Set project root
        self.root = Path(__file__).parent.parent

        # Load all associated criteria
        self._criteria = {}
        criteria_path = self.root / "criteria"
        for root, _, files in os.walk(criteria_path):
            for file in files:
                # Skip all non-json documents
                if '.json' not in file:
                    logger.warning(
                        'Criteria has received a non-valid json document: %s',
                        file
                    )
                    continue
                # Load criteria and save into internal _criteria attribute
                name, criteria = self._load_criteria(root, file)
                self._criteria[name] = criteria
    
    # Instance methods
    def _load_criteria(self, root:str, file:str):
        """Load given file as criteria."""
        path = os.path.join(root, file)
        roots, ext = self._parse_roots_ext(root, file)
        name = '.'.join(roots)

        logger.debug(
            'Processing criteria %s at %s.',
            '.'.join([name, ext]),
            path
        )

        # Load criteria
        criteria = []
        try:
            with open(path) as rules:
                criteria.extend(json.load(rules))
        except Exception as error:
            logger.error(
                'Criteria could not load %s due to %s',
                str(path),
                str(error)
            )
        else:
            return name, criteria
    
    def _parse_roots_ext(self, path, file):
        """Parse given file for name and qualified extension."""
        paths = str(path).replace(str(self.root), '').split('/')
        name, *exts = file.split('.')
        ext = '.'.join(exts) or ''

        paths.append(name)

        if len(paths) >= 2:
            paths = paths[1:]
            paths.remove('criteria')
            return paths, ext

        return None, None