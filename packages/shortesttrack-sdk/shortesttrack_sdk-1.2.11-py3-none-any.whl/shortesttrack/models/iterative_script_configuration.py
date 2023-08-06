from shortesttrack_tools.logger.utils import get_prototype_logger

from shortesttrack.models.base.model import Model

logger = get_prototype_logger('iterative-script-configuration')


class IterativeScriptConfiguration(Model):
    _id_key = 'uuid'

    def __str__(self):
        return f'ISSC({self.id})'
