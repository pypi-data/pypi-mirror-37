from shortesttrack_tools.api_client.endpoints import MetadataEndpoint, DataEndpoint
from shortesttrack_tools.functional import cached_property

from shortesttrack.utils import getLogger, APIClient

from collections import OrderedDict


logger = getLogger(__name__)


class SECHelper:
    def __init__(self, config_id=APIClient.CONFIGURATION_ID):
        logger.info(f'sec_id: {config_id}')
        self._config_id = config_id
        api_client = APIClient()
        self.metadata_endpoint = MetadataEndpoint(api_client=api_client, script_execution_configuration_id=config_id)
        self.data_endpoint = DataEndpoint(api_client=api_client, script_execution_configuration_id=config_id)

    @cached_property
    def sec(self) -> dict:
        return self.metadata_endpoint.request(self.metadata_endpoint.GET,
                                              f'script-execution-configurations/{self._config_id}')

    @cached_property
    def script_content(self) -> bytes:
        logger.info(f'get script content')
        return self.data_endpoint.request(self.data_endpoint.GET, f'script-execution-configurations/'
                                          f'{self._config_id}/script/content', raw_content=True)

    def get_matrix(self, matrix_id: str) -> OrderedDict:
        logger.info(f'get_matrix {matrix_id}')
        matrix_raw = self.data_endpoint.request(self.data_endpoint.GET,
                                                f'script-execution-configurations/{self._config_id}/'
                                                f'matrices/{matrix_id}/data')

        return self.matrix_from_api_format_to_sdk_content(matrix_raw)

    def insert_matrix(self, matrix_id: str, fields: list, data):
        url = f'script-execution-configurations/{self._config_id}/matrices/{matrix_id}/insert'
        matrix_sdk_content = OrderedDict([('matrix', data,), ('fields', fields)])
        matrix_raw = self.matrix_from_sdk_content_to_api_format(matrix_sdk_content)
        logger.info(matrix_raw)
        self.data_endpoint.request(self.data_endpoint.POST, url, json=matrix_raw, raw_content=True)
        logger.info(f'success matrix insert {matrix_id}')

    @staticmethod
    def matrix_from_api_format_to_sdk_content(json: OrderedDict) -> OrderedDict:
        fields = json['schema']['fields']

        matrix = []
        if None is not json.get('rows'):
            for f in json['rows']:
                row = []
                for v in f['f']:
                    row.append(v.get('v'))
                matrix.append(row)

        return OrderedDict([
            ('fields', fields,),
            ('matrix', matrix,),
        ])

    @staticmethod
    def matrix_from_sdk_content_to_api_format(content: OrderedDict) -> OrderedDict:
        insert_rows = []
        for row in content.get('matrix'):
            tmp = OrderedDict()
            for field, v in zip(content['fields'], row):
                tmp[field] = v
            insert_rows.append({"json": tmp})

        body = OrderedDict([('rows', insert_rows,)])

        return body
