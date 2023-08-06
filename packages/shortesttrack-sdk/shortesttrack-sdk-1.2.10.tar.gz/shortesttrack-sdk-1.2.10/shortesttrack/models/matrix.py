from collections import OrderedDict
from typing import Union

from shortesttrack_tools.functional import cached_property

from shortesttrack.models.base.model import Model


class Matrix(Model):
    _id_key = 'matrixId'

    def __init__(self, metadata):
        super().__init__(metadata)
        self._content = None

    def __str__(self):
        return f'Matrix({self.id})'

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
        self._content = self.get_matrix(self.id)
        return self

    def insert(self, fields: Union[list, OrderedDict], matrix_data):
        if isinstance(fields, OrderedDict):
            _fields = {f['name'] for f in fields}
            fields = _fields

        self.insert_matrix(self.id, fields, matrix_data)

    # Moved from SECHelper
    def get_matrix(self, matrix_id: str) -> dict:
        matrix_raw = self._lib.data_endpoint.get_matrix(matrix_id)
        return self.matrix_from_api_format_to_sdk_content(matrix_raw)

    @staticmethod
    def matrix_from_api_format_to_sdk_content(json_data: dict) -> dict:
        fields = json_data['schema']['fields']

        matrix = []
        if None is not json_data.get('rows'):
            for f in json_data['rows']:
                row = []
                for v in f['f']:
                    row.append(v.get('v'))
                matrix.append(row)

        return dict(
            fields=fields,
            matrix=matrix
        )

    @staticmethod
    def matrix_from_sdk_content_to_api_format(content: dict) -> dict:
        insert_rows = []
        for row in content.get('matrix'):
            tmp = {}
            for field, v in zip(content['fields'], row):
                tmp[field] = v
            insert_rows.append({"json": tmp})

        return dict(rows=insert_rows)

    def insert_matrix(self, matrix_id: str, fields: list, data):
        matrix_sdk_content = dict(matrix=data, fields=fields)
        matrix_raw = self.matrix_from_sdk_content_to_api_format(matrix_sdk_content)
        self._lib.data_endpoint.insert_matrix(matrix_id, matrix_raw)
