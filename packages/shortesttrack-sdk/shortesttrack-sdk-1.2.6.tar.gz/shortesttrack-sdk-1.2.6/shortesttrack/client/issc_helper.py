from shortesttrack_tools.api_client.endpoints import ExecAPIEndpoint
from shortesttrack_tools.functional import cached_property

from shortesttrack.utils import getLogger, APIClient

logger = getLogger()


class ISSCHelper:
    def __init__(self, issc_id=APIClient.ISSC_ID, sec_id=APIClient.CONFIGURATION_ID):
        logger.info(f'ISSC_ID: {issc_id} (SEC {sec_id})')
        self._issc_id = issc_id
        self._sec_id = sec_id
        api_client = APIClient()
        self.exec_api = ExecAPIEndpoint(api_client=api_client, script_execution_configuration_id=sec_id)

    @cached_property
    def issc(self) -> dict:
        path = f'issc/{self._issc_id}/'
        return self.exec_api.request(self.exec_api.GET, path)
