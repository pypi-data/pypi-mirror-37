from shortesttrack.client import SECHelper
from shortesttrack.utils import APIClient


class Matrix:
    def __init__(self, metadata, config_id=APIClient.CONFIGURATION_ID):
        self._metadata = metadata
        self._id = metadata['matrixId']
        self._helper = SECHelper(config_id=config_id)

    def read(self):
        return self._helper.get_matrix(self._id)

    def write(self, matrix_object):
        self._helper.insert_matrix(self._id, matrix_object)
