from shortesttrack_tools.api_client import endpoints
from shortesttrack_tools.unique import Unique

from shortesttrack.conf.lib_conf import ULibraryConfig
from shortesttrack.utils import APIClient
import typing

if typing.TYPE_CHECKING:
    from shortesttrack.models.script_configuration import ScriptConfiguration
    from shortesttrack.models.performance import Performance
    from shortesttrack.models.iterative_script_configuration import IterativeScriptConfiguration
    from shortesttrack.models.analytic_script_configuration import AnalyticScriptConfiguration


class ULibrary(Unique):
    api_client: APIClient = None
    metadata_endpoint: endpoints.MetadataEndpoint = None
    exec_api_endpoint: endpoints.ExecAPIEndpoint = None
    data_endpoint: endpoints.DataEndpoint = None
    exec_scheduler_endpoint: endpoints.ExecSchedulerEndpoint = None

    script_configuration: 'ScriptConfiguration' = None
    iterative_script_configuration: 'IterativeScriptConfiguration' = None
    analytic_script_configuration: 'AnalyticScriptConfiguration' = None
    performance: 'Performance' = None

    @classmethod
    def _do_init(cls, *args, **kwargs):
        from shortesttrack.models.script_configuration import ScriptConfiguration
        from shortesttrack.models.performance import Performance
        from shortesttrack.models.iterative_script_configuration import IterativeScriptConfiguration
        from shortesttrack.models.analytic_script_configuration import AnalyticScriptConfiguration

        # Fundamental objects
        cls.api_client = APIClient()
        cls.config = ULibraryConfig.init()
        script_configuration_id = cls.config.configuration_id

        # Endpoints
        cls.metadata_endpoint = endpoints.MetadataEndpoint(cls.api_client, script_configuration_id)
        cls.exec_api_endpoint = endpoints.ExecAPIEndpoint(cls.api_client, script_configuration_id)
        cls.data_endpoint = endpoints.DataEndpoint(cls.api_client, script_configuration_id)
        cls.exec_scheduler_endpoint = endpoints.ExecSchedulerEndpoint(cls.api_client, script_configuration_id)

        # Dynamic initialization
        if not cls.config.immutable_sec:
            # Config is not immutable, let's download it
            script_configuration_metadata = cls._download_sec()
        else:
            # Config is immutable, let's read it from file
            script_configuration_metadata = cls._read_sec(cls.config.immutable_sec_path)

        cls.script_configuration = ScriptConfiguration(script_configuration_metadata)

        if cls.config.iterative:
            # Initialize iterative things
            if not cls.config.immutable_issc:
                # Config is not immutable, let's download it
                issc_metadata = cls._download_issc(cls.config.issc_id)
            else:
                # Config is immutable, let's read it from file
                issc_metadata = cls._read_sec(cls.config.immutable_issc_path)
            cls.iterative_script_configuration = IterativeScriptConfiguration(issc_metadata)

        if cls.config.performance_id:
            # Initialize Performance things
            cls.performance = Performance(dict(id=cls.config.performance_id))

        if cls.config.asec_id:
            asec_metadata = cls._download_asec(cls.config.asec_id)
            cls.analytic_script_configuration = AnalyticScriptConfiguration(asec_metadata)

    @classmethod
    def _download_sec(cls):
        return cls.metadata_endpoint.script_execution_configuration

    @classmethod
    def _read_sec(cls, path):
        with open(path) as f:
            return f.read()

    @classmethod
    def _download_issc(cls, iscript_configuration_id):
        return cls.exec_api_endpoint.get_issc(iscript_configuration_id)

    @classmethod
    def _read_issc(cls, path):
        with open(path) as f:
            return f.read()

    @classmethod
    def _download_asec(cls, asec_id):
        path = f'iservice-asec/{asec_id}'
        return cls.exec_api_endpoint.request(cls.exec_api_endpoint.GET, path)
