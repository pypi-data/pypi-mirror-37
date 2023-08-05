from shortesttrack_tools.api_client.endpoints import ExecAPIEndpoint
from shortesttrack_tools.functional import cached_property

from shortesttrack.utils import getLogger, APIClient

logger = getLogger()


class ASECHelper:
    def __init__(self, asec_id=APIClient.ASEC_ID, sec_id=APIClient.CONFIGURATION_ID):
        logger.info(f'ASEC_ID {asec_id} (SEC {sec_id})')
        self._asec_id = asec_id
        self._sec_id = sec_id
        api_client = APIClient()
        self.exec_api_endpoint = ExecAPIEndpoint(api_client=api_client, script_execution_configuration_id=sec_id)

    @cached_property
    def asec(self) -> dict:
        path = f'iservice-asec/{self._asec_id}'
        return self.exec_api_endpoint.request(self.exec_api_endpoint.GET, path)
