from shortesttrack_tools.api_client.endpoints import MetadataEndpoint, DataEndpoint
from shortesttrack_tools.functional import cached_property

from shortesttrack.utils import getLogger, APIClient

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

    def get_matrix(self, matrix_id: str) -> dict:
        logger.info(f'get_matrix {matrix_id}')
        response = self.data_endpoint.request(self.data_endpoint.GET,
                                              f'script-execution-configurations/{self._config_id}/'
                                              f'matrices/{matrix_id}/data')
        fields = response['schema']['fields']

        matrix = []
        if None is not response.get('rows'):
            for f in response['rows']:
                row = []
                for v in f['f']:
                    row.append(v.get('v'))
                matrix.append(row)

        return {
            'fields': fields,
            'matrix': matrix
        }

    def insert_matrix(self, matrix_id: str, matrix: dict):
        url = f'script-execution-configurations/{self._config_id}/matrices/{matrix_id}/insert'

        logger.info(f'push matrix {matrix_id}')
        insert_rows = []
        for row in matrix.get('matrix'):
            tmp = {}
            for k, v in zip(matrix['fields'], row):
                tmp[k['name']] = v
            insert_rows.append({"json": tmp})

        body = {'rows': insert_rows}

        response = self.data_endpoint.request(self.data_endpoint.POST, url, json=body)

        logger.info(f'success matrix push {matrix_id} {insert_rows}: {response.content}')
