from collections import OrderedDict
from typing import Union

from shortesttrack_tools.functional import cached_property

from shortesttrack.client import SECHelper
from shortesttrack.utils import APIClient


class Matrix:
    def __init__(self, metadata, config_id=APIClient.CONFIGURATION_ID):
        self._metadata = metadata
        self._id = metadata['matrixId']
        self._helper = SECHelper(config_id=config_id)
        self._content = None

    @property
    def filled(self):
        return self._content is not None

    @property
    def data(self):
        return self._content['matrix']

    @cached_property
    def fields(self):
        return [f['name'] for f in self._content['fields']]

    def read(self):
        self._content = self._helper.get_matrix(self._id)
        return self

    def insert(self, fields: Union[list, OrderedDict], matrix_data):
        if isinstance(fields, OrderedDict):
            _fields = {f['name'] for f in fields}
            fields = _fields

        self._helper.insert_matrix(self._id, fields, matrix_data)
