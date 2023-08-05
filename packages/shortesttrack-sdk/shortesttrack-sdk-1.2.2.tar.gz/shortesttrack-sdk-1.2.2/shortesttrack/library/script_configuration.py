import json
import os
from typing import Dict

from shortesttrack_tools.functional import cached_property
from shortesttrack.client import SECHelper, PerformanceHelper
from shortesttrack.models.matrix import Matrix
from shortesttrack.utils import getLogger, APIClient

logger = getLogger()


class ScriptConfiguration:
    def __init__(self, sec_id: str = APIClient.CONFIGURATION_ID,
                 path_for_trained_model_data: str = 'trained_model.sav',
                 manual_data_manage: bool = False):
        logger.info(f'ScriptConfiguration {sec_id}')
        if not sec_id:
            raise Exception(f'SEC invalid configuration: {sec_id}')

        self._sec_id = sec_id
        self.helper = SECHelper(self._sec_id)
        self.sec = self.helper.sec
        self.path_for_trained_model_data = path_for_trained_model_data
        self._matrices_names = {}
        self._matrices = {}
        self._matrices_lists = {}

        if not manual_data_manage:
            self.__set_up_matrices()
            self.__set_up_trained_model()

    def __str__(self):
        return f'SEC({self._sec_id})'

    def __set_up_matrices(self) -> None:
        logger.info(f'setting up matrices...')
        for matrix in self.sec.get('matrices', []):
            self._matrices_names[matrix['id']] = matrix['matrixId']
            self._matrices[matrix['matrixId']] = Matrix(matrix)

        for matrix_list in self.sec.get('matricesLists', []):
            self._matrices_lists[matrix_list['id']] = dict()
            for matrix in matrix_list['matrices']:
                self._matrices_lists[matrix_list['id']][matrix['name']] = Matrix(matrix)

    def __set_up_trained_model(self) -> None:
        if not self.helper.trained_model_required:
            logger.info(f'trained model not required, skip setup')
            return

        logger.info(f'setting up trained model...')
        tm_data = self.helper.pull_trained_model_data()

        logger.info(f'writing trained model to file {os.path.abspath(self.path_for_trained_model_data)}')
        with open(self.path_for_trained_model_data, 'wb') as f:
            f.write(tm_data)

    @cached_property
    def matrices(self) -> dict:
        return self._matrices

    @property
    def matrices_lists(self) -> Dict[str, Dict[str, Matrix]]:
        return self._matrices_lists

    @cached_property
    def parameters(self) -> dict:
        return {
            p['id']: p.get('value') for p in self.sec.get('parameters', [])
        }

    def write_parameter(self, parameter_id, parameter_value, performance_id: str = APIClient.PERFORMANCE_ID,
                        parameter_type: str = 'default'):
        logger.info(f'writing output parameter to performance {performance_id}: {parameter_id}={parameter_value}')
        performance = PerformanceHelper(sec_id=self._sec_id, performance_id=performance_id)
        performance.write_parameter(parameter_id, parameter_value, parameter_type)

    def upload_trained_model(self, file_path: str, name: str) -> None:
        uploaded_tm = self.helper.upload_trained_model(file_path, name)
        logger.info(f'uploaded trained model {uploaded_tm}')

        if APIClient.PERFORMANCE_ID:
            self.write_parameter(parameter_id='trained_model', parameter_value=json.dumps(uploaded_tm),
                                 parameter_type='trained_model')
