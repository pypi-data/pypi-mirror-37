import requests
from urlobject import URLObject

from shortesttrack_tools.api_client.endpoints import MetadataEndpoint, DataEndpoint
from shortesttrack_tools.functional import cached_property
from shortesttrack.utils import getLogger, APIClient


logger = getLogger(__name__)


class SECHelper:
    def __init__(self, config_id: str = APIClient.CONFIGURATION_ID):
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

    @property
    def trained_model_required(self) -> bool:
        return self.sec.get('scriptOrSnapshot', {}).get('requiresTrainedModel', False)

    def get_matrix(self, matrix_id: str) -> dict:
        logger.info(f'get_matrix {matrix_id}')
        matrix_raw = self.data_endpoint.request(self.data_endpoint.GET,
                                                f'script-execution-configurations/{self._config_id}/'
                                                f'matrices/{matrix_id}/data')

        return self.matrix_from_api_format_to_sdk_content(matrix_raw)

    def insert_matrix(self, matrix_id: str, fields: list, data):
        url = f'script-execution-configurations/{self._config_id}/matrices/{matrix_id}/insert'
        matrix_sdk_content = dict(matrix=data, fields=fields)
        matrix_raw = self.matrix_from_sdk_content_to_api_format(matrix_sdk_content)
        logger.info(matrix_raw)
        self.data_endpoint.request(self.data_endpoint.POST, url, json=matrix_raw, raw_content=True)
        logger.info(f'success matrix insert {matrix_id}')

    @staticmethod
    def matrix_from_api_format_to_sdk_content(json: dict) -> dict:
        fields = json['schema']['fields']

        matrix = []
        if None is not json.get('rows'):
            for f in json['rows']:
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

    @cached_property
    def trained_model_id(self) -> str:
        return self.sec["trainedModelId"]

    @cached_property
    def trained_model(self) -> dict:
        """
        Response example: {
          "createdAt": "2018-10-17T04:21:45.203Z",
          "createdBy": "string",
          "fromSec": {
            "id": "string",
            "name": "string"
          },
          "id": "string",
          "modelName": "string",
          "modelUri": "string",
          "owner": "string",
          "secId": "string",
          "updatedAt": "2018-10-17T04:21:45.203Z",
          "updatedBy": "string",
          "version": 0
        }
        """
        trained_model_id = self.sec['trainedModelId']
        logger.info(f'get trained model {trained_model_id}')
        trained_model_raw = self.metadata_endpoint.request(self.metadata_endpoint.GET,
                                                           f'trained-models/{trained_model_id}')
        logger.info(f'trained model: {trained_model_raw}')
        return trained_model_raw

    @cached_property
    def trained_model_download_link(self) -> URLObject:
        logger.info(f'get trained model download link: {self.trained_model_id}')
        raw_url: bytes = self.data_endpoint.request(self.data_endpoint.GET,
                                                     f'trained-models/{self.trained_model_id}/download',
                                                     raw_content=True)
        logger.info(f'got raw link: {raw_url}')
        url = raw_url.decode("utf-8")
        return URLObject(url)

    def pull_trained_model_data(self) -> bytes:
        logger.info(f'download trained model data: {self.trained_model_id}')
        response = requests.get(self.trained_model_download_link)
        if response.status_code not in (200, 201):
            logger.error(f'{response.status_code, response.content}')
            raise Exception(f'Cannot download trained model data {self.trained_model_id}')

        logger.info(f'trained model downloaded {response.status_code}')
        return response.content

    def upload_trained_model(self, file_path: str, name: str) -> dict:
        logger.info(f'uploading trained model {name} ({file_path})...')
        with open(file_path, 'rb') as f:
            return self.data_endpoint.request(self.data_endpoint.POST,
                                              'trained-models/upload/',
                                              files={name: (name, f, 'multipart/form-data')})
