import logging

from shortesttrack.library import ScriptConfiguration

logger = logging.getLogger(__name__)


class TrainedModelMixin:
    def set_up_trained_model(self, path_for_trained_model_data: str = None):
        ScriptConfiguration(
            path_for_trained_model_data=path_for_trained_model_data,
            manual_data_manage=True
        ).download_trained_model()
