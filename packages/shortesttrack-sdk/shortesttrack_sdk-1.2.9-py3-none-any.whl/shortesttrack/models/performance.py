from shortesttrack_tools.logger.utils import get_prototype_logger

from shortesttrack.models.base.model import Model


logger = get_prototype_logger('performance')


class Performance(Model):
    def send_success(self):
        path = f'v1/sec/{self._lib.script_configuration.id}/performances/{self.id}/success/'
        self._lib.exec_scheduler_endpoint.request(self._lib.exec_scheduler_endpoint.POST, path, raw_content=True)

    def send_failed(self):
        path = f'v1/sec/{self._lib.script_configuration.id}/performances/{self.id}/failed/'
        self._lib.exec_scheduler_endpoint.request(self._lib.exec_scheduler_endpoint.POST, path, raw_content=True)

    def write_parameter(self, parameter_id: str, parameter_value: str, parameter_type: str = 'default'):
        path = f'performances/{self.id}/output-parameters/{parameter_id}/value/'

        body = {
            'value': parameter_value,
            'parameter_type': parameter_type
        }

        self._lib.exec_api_endpoint.request(self._lib.exec_api_endpoint.POST, path, json=body, raw_content=True)
