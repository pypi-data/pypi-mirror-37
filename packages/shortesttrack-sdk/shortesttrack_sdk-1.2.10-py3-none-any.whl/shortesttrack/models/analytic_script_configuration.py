from shortesttrack_tools.logger.utils import get_prototype_logger

from shortesttrack.client import ISSConnector
from shortesttrack.models.base.model import Model

logger = get_prototype_logger('analytic-script-configuration')


class ISSConnectionInfo:
    # TODO: move to a separate model
    def __init__(self, info: dict) -> None:
        self.url = info.get('url')
        self.url = self.url if self.url[-1] != '/' else self.url[0:-1]
        self.auth_custom_token = info.get('auth_custom_token')
        self.id = info.get('iscript_service_id')


class AnalyticScriptConfiguration(Model):
    _id_key = 'uuid'

    def __str__(self):
        return f'ASEC({self.id})'

    def get_iss_connection_info(self) -> list:
        return [ISSConnectionInfo(info) for info in self.metadata['relations']]

    @staticmethod
    def get_iss_connector(connection_info: ISSConnectionInfo) -> ISSConnector:
        return ISSConnector(
            url=connection_info.url, auth_custom_token=connection_info.auth_custom_token
        )
