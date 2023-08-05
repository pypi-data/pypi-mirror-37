from shortesttrack_tools.functional import cached_property

from shortesttrack.client import SECHelper, PerformanceHelper
from shortesttrack.models.matrix import Matrix
from shortesttrack.utils import getLogger, APIClient

logger = getLogger()


class ScriptConfiguration:
    def __init__(self, sec_id=APIClient.CONFIGURATION_ID):
        logger.info(f'ScriptConfiguration {sec_id}')
        if not sec_id:
            raise Exception(f'SEC invalid configuration: {sec_id}')

        self._sec_id = sec_id
        self.helper = SECHelper(self._sec_id)
        self.sec = self.helper.sec
        self._matrices_names = {}
        self._matrices = {}
        self._matrices_lists = {}

        for matrix in self.sec.get('matrices', []):
            self._matrices_names[matrix['id']] = matrix['matrixId']
            self._matrices[matrix['matrixId']] = Matrix(matrix)

        for matrix_list in self.sec.get('matricesLists', []):
            self._matrices_lists[matrix_list['id']] = dict()
            for matrix in matrix_list['matrices']:
                self._matrices_lists[matrix_list['id']][matrix['name']] = Matrix(matrix)

    def __str__(self):
        return f'SEC({self._sec_id})'

    @cached_property
    def matrices(self) -> dict:
        return self._matrices

    @property
    def matrices_lists(self) -> dict:
        return self._matrices_lists

    @cached_property
    def parameters(self) -> dict:
        return {
            p['id']: p.get('value') for p in self.sec.get('parameters', [])
        }

    def write_parameter(self, parameter_id, parameter_value, performance_id: str = APIClient.PERFORMANCE_ID):
        performance = PerformanceHelper(
            sec_id=self._sec_id, performance_id=performance_id
        )
        performance.write_parameter(
            parameter_id=parameter_id, parameter_value=parameter_value
        )
