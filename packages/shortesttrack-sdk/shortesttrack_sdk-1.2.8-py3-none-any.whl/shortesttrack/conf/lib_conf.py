import os

from shortesttrack_tools.unique import Unique


class ULibraryConfig(Unique):
    sec_refresh_token = None
    issc_id = None
    configuration_id = None
    asec_id = None
    performance_id = None

    iterative: bool = None

    immutable_sec: bool = None
    immutable_sec_path: str = None

    immutable_issc: bool = None
    immutable_issc_path: str = None

    trained_model_data_path: str = None
    manual_data_manage: bool = None

    @classmethod
    def _do_init(
            cls,
            sec_refresh_token=None,
            issc_id=None,
            configuration_id=None,
            asec_id=None,
            performance_id=None,
            iterative=False,
            immutable_sec=False,
            immutable_sec_path=None,
            immutable_issc=False,
            immutable_issc_path=None,
            trained_model_data_path=None,
            manual_data_manage=False
    ):

        cls.sec_refresh_token = sec_refresh_token or os.getenv('SEC_REFRESH_TOKEN')
        cls.issc_id = issc_id or os.getenv('ISSC_ID')
        cls.configuration_id = configuration_id or os.getenv('CONFIGURATION_ID')
        cls.asec_id = asec_id or os.getenv('ASEC_ID')
        cls.performance_id = performance_id or os.getenv('PERFORMANCE_ID')

        if immutable_sec:
            assert immutable_sec_path

        if immutable_issc:
            assert immutable_issc_path

        cls.iterative = iterative
        cls.immutable_sec = immutable_sec
        cls.immutable_sec_path = immutable_sec_path
        cls.immutable_issc = immutable_issc
        cls.immutable_issc_path = immutable_issc_path
        cls.trained_model_data_path = trained_model_data_path
        cls.manual_data_manage = manual_data_manage
