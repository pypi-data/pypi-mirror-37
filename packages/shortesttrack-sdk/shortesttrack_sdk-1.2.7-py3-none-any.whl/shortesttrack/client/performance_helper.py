from shortesttrack_tools.api_client.endpoints import ExecSchedulerEndpoint, ExecAPIEndpoint

from shortesttrack.utils import getLogger, APIClient

logger = getLogger(__name__)


class PerformanceHelper:
    def __init__(self, performance_id=APIClient.PERFORMANCE_ID, sec_id=APIClient.CONFIGURATION_ID):
        logger.info(f'PerformanceHelper performance_id: {performance_id} sec_id: {sec_id}')
        self._sec_id = sec_id
        self._performance_id = performance_id
        api_client = APIClient()
        self.exec_scheduler_endpoint = ExecSchedulerEndpoint(api_client, sec_id)
        self.exec_api_endpoint = ExecAPIEndpoint(api_client, sec_id)

    def send_success(self):
        path = f'v1/sec/{self._sec_id}/performances/{self._performance_id}/success/'
        self.exec_scheduler_endpoint.request(self.exec_scheduler_endpoint.POST, path, raw_content=True)

    def send_failed(self):
        path = f'v1/sec/{self._sec_id}/performances/{self._performance_id}/failed/'
        self.exec_scheduler_endpoint.request(self.exec_scheduler_endpoint.POST, path, raw_content=True)

    def write_parameter(self, parameter_id: str, parameter_value: str, parameter_type: str = 'default'):
        path = f'performances/{self._performance_id}/output-parameters/{parameter_id}/value/'

        body = {
            'value': parameter_value,
            'parameter_type': parameter_type
        }

        self.exec_api_endpoint.request(self.exec_api_endpoint.POST, path, json=body, raw_content=True)
