from shortesttrack.client import ASECHelper, ISSConnector
from shortesttrack.library.script_configuration import ScriptConfiguration
from shortesttrack.utils import getLogger, APIClient

logger = getLogger()


class ISSConnectionInfo:
    def __init__(self, info: dict) -> None:
        self.url = info.get('url')
        self.url = self.url if self.url[-1] != '/' else self.url[0:-1]
        self.auth_custom_token = info.get('auth_custom_token')
        self.id = info.get('iscript_service_id')


class AnalyticScriptConfiguration(ScriptConfiguration):
    def __init__(self, asec_id: str = APIClient.ASEC_ID) -> None:
        logger.info(f'AnalyticScriptConfiguration {asec_id}')
        if not asec_id:
            raise Exception('No ASEC found')

        self.asec_id = asec_id
        self._asec = ASECHelper(self.asec_id).asec
        super().__init__(self._asec['configuration_id'])

    def __str__(self):
        return f'ASEC({self.asec_id})'

    def get_iss_connection_info(self) -> list:
        return [ISSConnectionInfo(info) for info in self._asec['relations']]

    @staticmethod
    def get_iss_connector(connection_info: ISSConnectionInfo) -> ISSConnector:
        return ISSConnector(
            url=connection_info.url, auth_custom_token=connection_info.auth_custom_token
        )
