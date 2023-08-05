import unittest
from unittest.mock import patch
import xmlrunner
import azureml.data.constants as constants
from azureml.core.conda_dependencies import TENSORFLOW_PACKAGE_PREFIX
from azureml.core.compute_target import LocalTarget
from azureml.core.experiment import Experiment
from azureml.core.runconfig import DEFAULT_GPU_IMAGE, EnvironmentDefinition
from azureml.data.data_reference import DataReference
from azureml.data.abstract_datastore import AbstractDatastore
from azureml.data.azure_storage_datastore import AbstractAzureStorageDatastore
from mock_objects import MockObjects
from azureml.train.dnn import TensorFlow, _TensorFlowRunConfiguration


class TensorflowUnitTests(unittest.TestCase):
    NCCL_SOCKET_IFNAME_KEY = 'NCCL_SOCKET_IFNAME'
    DOCKER0_KEY = '^docker0'
    DATA_STORE_NAME = "datastore"
    TRAIN_DATA_REF_NAME = "traindata"
    TEST_DATA_REF_NAME = "testdata"
    PATH_ON_DATA_STORE = "train"
    CONTAINER_NAME = "test_container"
    ACCOUNT_NAME = "testaccount"

    def setUp(self):
        self._project_folder = MockObjects.get_project_folder()
        self._mock_workspace = MockObjects.get_workspace()
        self._mock_compute_target = MockObjects.get_compute_target_batchai()
        self._mock_compute_target_local = MockObjects.get_compute_target_local()
        self._mock_datastore = AbstractDatastore(
            workspace=self._mock_workspace,
            name=self.DATA_STORE_NAME,
            datastore_type="AzureBlob")
        self._mock_data_ref_train = DataReference(
            datastore=self._mock_datastore,
            data_reference_name=self.TRAIN_DATA_REF_NAME,
            path_on_datastore=self.PATH_ON_DATA_STORE)
        self._mock_data_ref_test = AbstractAzureStorageDatastore(
            self._mock_workspace,
            self.DATA_STORE_NAME,
            constants.AZURE_BLOB,
            self.CONTAINER_NAME,
            self.ACCOUNT_NAME)
        self._experiment = Experiment(self._mock_workspace, "tf_unittest")

    @patch('azureml.core.runconfig.RunConfiguration.save')
    def test_tf_run_configuration(self, mock_run_config_save):
        mock_run_config_save.return_val = ""

        tf_run_config = _TensorFlowRunConfiguration(
            self._mock_compute_target,
            entry_script="testscript.py",
            script_params={},
            node_count=3,
            process_count_per_node=1,
            use_gpu=True,
            distributed_backend="mpi",
            use_docker=False,
            custom_docker_base_image=None,
            conda_packages=None,
            pip_packages=None,
            environment_definition=None,
            inputs=None
        )
        assert self.NCCL_SOCKET_IFNAME_KEY in \
            tf_run_config.environment.environment_variables
        assert tf_run_config.environment.\
            environment_variables[self.NCCL_SOCKET_IFNAME_KEY] \
            == self.DOCKER0_KEY
        assert tf_run_config.batchai.node_count == 3

    @patch('azureml.core.conda_dependencies.CondaDependencies.save_to_file')
    def test_tf_conda_dependencies(self, mock_conda_dependencies_file):
        mock_conda_dependencies_file.return_value = "aml_config/test_conda_dependencies.yaml"
        tf_estimator = TensorFlow(self._project_folder, compute_target=self._mock_compute_target,
                                  distributed_backend="ps")
        assert (len(tf_estimator.conda_dependencies.
                    _get_conda_package_with_prefix(TENSORFLOW_PACKAGE_PREFIX)) > 0 or
                len(tf_estimator.conda_dependencies.
                    _get_pip_package_with_prefix(TENSORFLOW_PACKAGE_PREFIX)) > 0)

    def test_tf_run_configuration_custom_docker(self):
        image_repo = MockObjects.get_image_repo()
        env_def = EnvironmentDefinition()
        base_img_name = 'some base image'
        env_def.docker.base_image = base_img_name
        env_def.docker.enabled = True
        env_def.docker.base_image_registry = image_repo

        tf = TensorFlow(
            self._project_folder,
            compute_target=self._mock_compute_target,
            entry_script="testscript.py",
            script_params={},
            node_count=3,
            distributed_backend="mpi",
            process_count_per_node=1,
            environment_definition=env_def
        )
        # assert self.NCCL_SOCKET_IFNAME_KEY in cntk.run_config.environment.environment_variables
        # assert cntk.run_config.environment.environment_variables[self.NCCL_SOCKET_IFNAME_KEY] == self.DOCKER0_KEY
        assert tf.run_config.batchai.node_count == 3
        assert tf.run_config.environment.docker.base_image == base_img_name
        assert tf.run_config.environment.docker.base_image_registry.address == image_repo.address
        assert tf.run_config.environment.docker.base_image_registry.password == image_repo.password
        assert tf.run_config.environment.docker.base_image_registry.username == image_repo.username
        self.assertTrue(tf.run_config.environment.docker.enabled)
        self.assertFalse(tf.run_config.environment.python.user_managed_dependencies)
        self.assertTrue(tf.run_config.auto_prepare_environment)
        self.assertTrue(tf.run_config.environment.spark.precache_packages)

    def test_tf_local_compute(self):
        base_docker_image = "hesuri/mmlspark"

        local_compute_target = LocalTarget()

        # validate local compute target without docker
        tf_estimator = TensorFlow(self._project_folder, node_count=1, compute_target=local_compute_target)
        assert tf_estimator._compute_target.type == LocalTarget._LOCAL_TYPE
        assert tf_estimator._compute_target.name == "local"
        self.assertTrue(tf_estimator.run_config.environment.docker.enabled)

        # validate local compute target with docker
        tf_estimator = TensorFlow(self._project_folder, node_count=1, compute_target=local_compute_target,
                                  custom_docker_base_image=base_docker_image)
        assert tf_estimator._compute_target.type == LocalTarget._LOCAL_TYPE
        assert tf_estimator._compute_target.name == "local"
        self.assertTrue(tf_estimator.run_config.environment.docker.enabled)
        assert tf_estimator.run_config.environment.docker.base_image == base_docker_image

        # validate local compute target with gpu based docker
        tf_estimator = TensorFlow(self._project_folder, node_count=1, compute_target=local_compute_target,
                                  use_gpu=True, distributed_backend="mpi")
        assert tf_estimator._compute_target.type == LocalTarget._LOCAL_TYPE
        assert tf_estimator._compute_target.name == "local"
        self.assertTrue(tf_estimator.run_config.environment.docker.enabled)
        assert tf_estimator.run_config.environment.docker.base_image == DEFAULT_GPU_IMAGE

    def test_tf_distrib_compute(self):
        tf_estimator = TensorFlow(self._project_folder, compute_target=self._mock_compute_target)
        self.assertEqual("Python", tf_estimator._estimator_config.framework)
        tf_estimator = TensorFlow(self._project_folder, compute_target=self._mock_compute_target, node_count=1)
        self.assertEqual("Python", tf_estimator._estimator_config.framework)
        tf_estimator = TensorFlow(self._project_folder, compute_target=self._mock_compute_target,
                                  process_count_per_node=2, distributed_backend="mpi")
        self.assertEqual("PythonMpi", tf_estimator._estimator_config.framework)
        tf_estimator = TensorFlow(self._project_folder, compute_target=self._mock_compute_target,
                                  process_count_per_node=2, node_count=4, distributed_backend="mpi")
        self.assertEqual("PythonMpi", tf_estimator._estimator_config.framework)

    def test_tf_user_managed_dependencies(self):
        tf_estimator = TensorFlow(self._project_folder, node_count=1, compute_target=self._mock_compute_target)
        self.assertFalse(tf_estimator.run_config.environment.python.user_managed_dependencies)

    def get_last_conda_deps(self, estimator):
        return estimator._last_submitted_runconfig.environment.python.conda_dependencies

    @patch('azureml.train.estimator.MMLBaseEstimator._fit')
    def test_tf_negative(self, mock_fit):
        try:
            TensorFlow(self._project_folder, compute_target=self._mock_compute_target_local, node_count=2,
                       distributed_backend="mpi")
            raise Exception("Exception should be thrown but was not.")
        except Exception as ex:
            self.assertEqual('Compute target should be Batch AI for distributed training (node_count > 1).',
                             str(ex))

    def test_tf_datastore_inputs(self):
        print("\ntest_tf_datastore_inputs")
        test_inputs = [self._mock_data_ref_train, self._mock_data_ref_test]
        tf_estimator = TensorFlow(
            self._project_folder, compute_target=self._mock_compute_target,
            inputs=test_inputs)
        self.assertEqual(2, len(tf_estimator.run_config.data_references))
        dref = tf_estimator.run_config.data_references['traindata']
        self._validate_train_data_ref(dref)
        df_keys = list(tf_estimator.run_config.data_references.keys())
        self.assertIn(self._mock_data_ref_train.data_reference_name, df_keys)
        self.assertIn(self._mock_data_ref_test._data_reference.data_reference_name, df_keys)

    def test_tf_datastore_script_params_duplicate_removed(self):
        print("\ntest_tf_datastore_script_params_duplicate_removed")
        script_params = {"train": self._mock_data_ref_train}
        tf_estimator = TensorFlow(
            self._project_folder, compute_target=self._mock_compute_target,
            script_params=script_params, inputs=[self._mock_data_ref_train])
        self.assertEqual(1, len(tf_estimator.run_config.data_references))
        dref = tf_estimator.run_config.data_references['traindata']
        self._validate_train_data_ref(dref)
        self.assertEqual(2, len(tf_estimator.run_config.arguments))
        self.assertEqual(
            "$AZUREML_DATAREFERENCE_traindata",
            tf_estimator.run_config.arguments[1])

    @patch('azureml.train.estimator.MMLBaseEstimator._fit')
    def test_tf_datastore_fit_override(self, mock_fit):
        tf_estimator = TensorFlow(
            self._project_folder, compute_target=self._mock_compute_target,
            inputs=[self._mock_data_ref_train])
        self.assertEqual(1, len(tf_estimator.run_config.data_references))

        dref = tf_estimator.run_config.data_references['traindata']
        self._validate_train_data_ref(dref)

        self._experiment.submit(tf_estimator, inputs=[self._mock_data_ref_test])
        self.assertEqual(1, len(tf_estimator.run_config.data_references))

    def _validate_train_data_ref(self, dref):
        self.assertEqual(TensorflowUnitTests.DATA_STORE_NAME, dref.data_store_name)
        self.assertEqual(TensorflowUnitTests.PATH_ON_DATA_STORE, dref.path_on_data_store)
        self.assertEqual('mount', dref.mode)

    def test_tf_run_config_custom_image_user_managed(self):
        image_repo = MockObjects.get_image_repo()
        env_def = EnvironmentDefinition()
        base_img_name = 'some base image'
        env_def.docker.base_image = base_img_name
        env_def.docker.enabled = True
        env_def.docker.base_image_registry = image_repo
        env_def.python.user_managed_dependencies = True

        tf = TensorFlow(
            MockObjects.get_project_folder(),
            compute_target=self._mock_compute_target,
            entry_script="testscript.py",
            script_params={},
            node_count=3,
            process_count_per_node=1,
            environment_definition=env_def,
            distributed_backend="mpi"
        )
        print("BASE IMAGE:{}".format(tf.run_config.environment.docker.base_image))
        assert tf.run_config.environment.docker.base_image == base_img_name
        assert tf.run_config.environment.docker.base_image_registry.address == image_repo.address
        assert tf.run_config.environment.docker.base_image_registry.password == image_repo.password
        assert tf.run_config.environment.docker.base_image_registry.username == image_repo.username
        self.assertTrue(tf.run_config.environment.docker.enabled)
        self.assertTrue(tf.run_config.environment.python.user_managed_dependencies)
        self.assertTrue(tf.run_config.auto_prepare_environment)
        self.assertFalse(tf.run_config.environment.spark.precache_packages)

    @patch('azureml.train.estimator.MMLBaseEstimator._fit')
    def test_estimator_negative(self, mock_fit):
        with self.assertRaisesRegex(Exception, "should be Batch AI for distributed training"):
            TensorFlow(self._project_folder, compute_target=self._mock_compute_target_local, node_count=2,
                       distributed_backend="mpi")

    @patch('azureml.train.estimator.MMLBaseEstimator._fit')
    def test_estimator_fit_negative(self, mock_fit):
        with self.assertRaisesRegex(Exception, "should be Batch AI for distributed training"):
            TensorFlow(self._project_folder, compute_target=self._mock_compute_target_local, node_count=2,
                       distributed_backend="mpi")

    @patch('azureml.train.estimator.MMLBaseEstimator._submit')
    @patch('azureml.core.conda_dependencies.CondaDependencies.save_to_file')
    @patch('azureml.core.runconfig.RunConfiguration.save')
    def test_tf_fit_override_script_params(self, mock_run_config, mock_conda_dependencies, mock_submit):
        estimator = TensorFlow(self._project_folder, compute_target=self._mock_compute_target)
        self._experiment.submit(estimator, script_params={"param1": "value1"})
        self.assertEqual(2, len(estimator._last_submitted_runconfig.arguments))
        self.assertTrue("param1" in estimator._last_submitted_runconfig.arguments)
        self.assertTrue("value1" in estimator._last_submitted_runconfig.arguments)

        estimator = TensorFlow(self._project_folder, compute_target=self._mock_compute_target,
                               script_params={"param1": "value1"})
        self._experiment.submit(estimator, script_params={"param2": "value2"})
        self.assertEqual(4, len(estimator._last_submitted_runconfig.arguments))
        self.assertTrue("param1" in estimator._last_submitted_runconfig.arguments)
        self.assertTrue("value1" in estimator._last_submitted_runconfig.arguments)
        self.assertTrue("param2" in estimator._last_submitted_runconfig.arguments)
        self.assertTrue("value2" in estimator._last_submitted_runconfig.arguments)


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner())
