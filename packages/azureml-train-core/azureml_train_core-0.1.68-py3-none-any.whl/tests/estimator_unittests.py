import unittest
from unittest.mock import patch
import xmlrunner
import json
import azureml.data.constants as constants
from azureml.core.experiment import Experiment
from mock_objects import MockObjects
from azureml.core.runconfig import EnvironmentDefinition, DEFAULT_CPU_IMAGE, DEFAULT_GPU_IMAGE
from azureml.train.estimator import Estimator
from azureml.data.data_reference import DataReference
from azureml.data.abstract_datastore import AbstractDatastore
from azureml.data.azure_storage_datastore import AbstractAzureStorageDatastore


class EstimatorUnitTests(unittest.TestCase):
    DATA_STORE_NAME = "datastore"
    TRAIN_DATA_REF_NAME = "traindata"
    TEST_DATA_REF_NAME = "testdata"
    PATH_ON_DATA_STORE = "train"
    CONTAINER_NAME = "test_container"
    ACCOUNT_NAME = "testaccount"
    # TODO: set this to 1 when psutil dependency is restored
    psutil = 0

    def setUp(self):
        self._mock_workspace = MockObjects.get_workspace()
        self._project_folder = MockObjects.get_project_folder()
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
        self._experiment = Experiment(self._mock_workspace, "estimator_unittest")

    def validate_estimator_config(self, est, script='train.py', args=[], user_deps=False,
                                  docker_enabled=True, use_gpu=False, docker_base_image=DEFAULT_CPU_IMAGE,
                                  conda_packages_count=1, pip_packages_count=1):
        self.assertEqual(script, est.run_config.script)
        self.assertEqual(len(args), len(est.run_config.arguments))
        self.assertEqual(user_deps, est.run_config.environment.python.user_managed_dependencies)
        self.assertEqual(docker_enabled, est.run_config.environment.docker.enabled)
        self.assertEqual(use_gpu, est.run_config.environment.docker.gpu_support)
        self.assertIsNotNone(est.conda_dependencies)
        self.assertEqual(docker_base_image, est.run_config.environment.docker.base_image)
        conda_packages = est.conda_dependencies.conda_packages
        # python and psutil included by default and hence default value for conda_packages_count is 2
        self.assertEqual(conda_packages_count + self.psutil, sum(1 for _ in conda_packages))
        # index-url, extra-index-url and azureml-sdk included default
        self.assertEqual(pip_packages_count, sum(1 for _ in est.conda_dependencies.pip_packages))

    def test_estimator_default_env(self):
        est = Estimator(self._project_folder, compute_target=self._mock_compute_target)
        self.validate_estimator_config(est)
        self.assertEqual("Python", est._estimator_config.framework)

    def test_estimator_additional_pip_pkg(self):
        est = Estimator(self._project_folder, compute_target=self._mock_compute_target,
                        pip_packages=['some package', 'some other package'])
        # index-url, extra-index-url and azureml-sdk included default
        self.assertEqual(3, sum(1 for _ in est.conda_dependencies.pip_packages))

    def test_estimator_additional_conda_pkg(self):
        est = Estimator(self._project_folder, compute_target=self._mock_compute_target,
                        conda_packages=['some package', 'some other pkg', 'yet another pkg'])
        #  python and psutil included by default
        for _ in est.conda_dependencies.conda_packages:
            print(_)
        self.assertEqual(4 + self.psutil, sum(1 for _ in est.conda_dependencies.conda_packages))

    def test_estimator_use_gpu_setter(self):
        est = Estimator(self._project_folder, compute_target=self._mock_compute_target, use_gpu=True)
        self.assertTrue(est.run_config.environment.docker.gpu_support)
        self.assertEqual(DEFAULT_GPU_IMAGE, est.run_config.environment.docker.base_image)
        self.assertEqual("Python", est.run_config.framework)

        img_name = 'some image name'
        est = Estimator(self._project_folder, compute_target=self._mock_compute_target, use_gpu=True,
                        custom_docker_base_image=img_name)
        self.assertTrue(est.run_config.environment.docker.gpu_support)
        self.assertEqual(img_name, est.run_config.environment.docker.base_image)

    def test_estimator_use_docker_setter(self):
        est = Estimator(self._project_folder, compute_target=self._mock_compute_target, use_docker=False)
        self.assertFalse(est.run_config.environment.docker.enabled)

    def test_estimator_docker_image_setter(self):
        img_name = 'some image name'
        est = Estimator(self._project_folder, compute_target=self._mock_compute_target,
                        custom_docker_base_image=img_name)
        self.assertFalse(est.run_config.environment.docker.gpu_support)
        self.assertEqual(img_name, est.run_config.environment.docker.base_image)

    def test_estimator_custom_env(self):
        custom_env = EnvironmentDefinition()
        custom_env.python.user_managed_dependencies = True
        est = Estimator(self._project_folder, compute_target=self._mock_compute_target,
                        environment_definition=custom_env)
        self.assertEqual(est.run_config.environment, custom_env)

    def test_estimator_pip_env_both(self):
        with self.assertRaises(Exception):
            custom_env = EnvironmentDefinition()
            custom_env.python.user_managed_dependencies = True
            Estimator(self._project_folder, compute_target=self._mock_compute_target,
                      environment_definition=custom_env, pip_packages=['some package'])

    def test_estimator_conda_env_both(self):
        with self.assertRaises(Exception):
            environment_definition = EnvironmentDefinition()
            environment_definition.python.user_managed_dependencies = True
            Estimator(self._project_folder, compute_target=self._mock_compute_target,
                      environment_definition=environment_definition, conda_packages=['some package'])

    def test_estimator_docker_image_env_both(self):
        with self.assertRaises(Exception):
            Estimator(self._project_folder, compute_target=self._mock_compute_target,
                      environment_definition=EnvironmentDefinition(), custom_docker_base_image='some image')

    def test_estimator_gpu_env_both(self):
        with self.assertRaises(Exception):
            Estimator(self._project_folder, compute_target=self._mock_compute_target,
                      environment_definition=EnvironmentDefinition(), use_gpu=True)

    def test_estimator_use_docker_false_custom_image_set(self):
        with self.assertRaises(Exception):
            Estimator(self._project_folder, compute_target=self._mock_compute_target, use_docker=False,
                      custom_docker_base_image='some image')

    def test_estimator_fit_conda_env_both(self):
        est = Estimator(self._project_folder, compute_target=self._mock_compute_target,
                        conda_packages=['some package'])
        with self.assertRaises(Exception):
            self._experiment.submit(est, environment_definition=EnvironmentDefinition())

    def test_estimator_fit_docker_image_env_both(self):
        img_name = 'some image name'
        est = Estimator(self._project_folder, compute_target=self._mock_compute_target,
                        custom_docker_base_image=img_name)
        with self.assertRaises(Exception):
            self._experiment.submit(est, environment_definition=EnvironmentDefinition())

    def test_estimator_fit_gpu_env_both(self):
        est = Estimator(self._project_folder, compute_target=self._mock_compute_target,
                        use_gpu=True)
        with self.assertRaises(Exception):
            self._experiment.submit(est, environment_definition=EnvironmentDefinition())

    def test_estimator_fit_use_docker_false_custom_image_set(self):
        est = Estimator(self._project_folder, compute_target=self._mock_compute_target,
                        custom_docker_base_image='some image')
        with self.assertRaises(Exception):
            self._experiment.submit(est, use_docker=True)

    def test_estimator_fit_use_docker_false_custom_image_set_2(self):
        est = Estimator(self._project_folder, compute_target=self._mock_compute_target, use_docker=False)
        with self.assertRaises(Exception):
            self._experiment.submit(est, custom_docker_base_image='some image')

    @patch('azureml.train.estimator.MMLBaseEstimator._submit')
    def test_estimator_fit_override_script(self, mock_fit):
        est = Estimator(self._project_folder, compute_target=self._mock_compute_target,
                        entry_script='myscript.py')
        self.validate_estimator_config(est, script='myscript.py')
        self._experiment.submit(est, entry_script='anotherscript.py')
        # validate original estimator
        self.validate_estimator_config(est, script='myscript.py')

    @patch('azureml.train.estimator.MMLBaseEstimator._submit')
    def test_estimator_fit_override_script_args(self, mock_fit):
        est = Estimator(self._project_folder, compute_target=self._mock_compute_target,
                        entry_script='myscript.py', script_params={"arg1": 123, "arg2": "value"})
        self.validate_estimator_config(est, script='myscript.py', args=['arg1', 123, 'arg2', 'value'])
        self.assertEqual(4, len(est.run_config.arguments))
        self.assertEqual(1, est.run_config.arguments.count("arg1"))
        self.assertEqual(1, est.run_config.arguments.count(123))
        self.assertEqual(1, est.run_config.arguments.count("arg2"))
        self.assertEqual(1, est.run_config.arguments.count("value"))
        self._experiment.submit(est, script_params={"arg1": 456, "arg3": "value3"})
        # validate original estimator
        self.assertEqual(4, len(est.run_config.arguments))
        self.assertEqual(1, est.run_config.arguments.count("arg1"))
        self.assertEqual(1, est.run_config.arguments.count(123))
        self.assertEqual(1, est.run_config.arguments.count("arg2"))
        self.assertEqual(1, est.run_config.arguments.count("value"))

        self.assertEqual(6, len(est._last_submitted_runconfig.arguments))
        self.assertEqual(1, est._last_submitted_runconfig.arguments.count("arg1"))
        self.assertEqual(1, est._last_submitted_runconfig.arguments.count(456))
        self.assertEqual(1, est._last_submitted_runconfig.arguments.count("arg2"))
        self.assertEqual(1, est._last_submitted_runconfig.arguments.count("value"))
        self.assertEqual(1, est._last_submitted_runconfig.arguments.count("arg3"))
        self.assertEqual(1, est._last_submitted_runconfig.arguments.count("value3"))

    @patch('azureml.train.estimator.MMLBaseEstimator._submit')
    def test_estimator_fit_override_pip_packages(self, mock_fit):
        est = Estimator(self._project_folder, compute_target=self._mock_compute_target,
                        pip_packages=['some pkg1', 'duplicate pkg'])
        self.validate_estimator_config(est, pip_packages_count=3)
        self._experiment.submit(est, pip_packages=['some other pkg3', 'duplicate pkg'])
        # validate original estimator
        self.validate_estimator_config(est, pip_packages_count=3)
        self.assertTrue("some other pkg3" in pkg for pkg in est._last_submitted_runconfig.environment.python.
                        conda_dependencies.pip_packages)

    def test_datastore_inputs(self):
        test_inputs = [self._mock_data_ref_train, self._mock_data_ref_test]
        es = Estimator(
            self._project_folder, compute_target=self._mock_compute_target,
            inputs=test_inputs)

        self.assertEqual(2, len(es.run_config.data_references))
        dref = es.run_config.data_references['traindata']
        self._validate_train_data_ref(dref)

        df_keys = list(es.run_config.data_references.keys())
        self.assertIn(self._mock_data_ref_train.data_reference_name, df_keys)
        self.assertIn(self._mock_data_ref_test._data_reference.data_reference_name, df_keys)

    def test_datastore_script_params_duplicate_removed(self):
        script_params = {"train": self._mock_data_ref_train}
        es = Estimator(
            self._project_folder, compute_target=self._mock_compute_target,
            script_params=script_params, inputs=[self._mock_data_ref_train])
        self.assertEqual(1, len(es.run_config.data_references))

        dref = es.run_config.data_references['traindata']
        self._validate_train_data_ref(dref)
        self.assertEqual(2, len(es.run_config.arguments))
        self.assertEqual(
            "$AZUREML_DATAREFERENCE_traindata",
            es.run_config.arguments[1])

    @patch('azureml.train.estimator.MMLBaseEstimator._submit')
    def test_datastore_fit_override_inputs(self, mock_fit):
        es = Estimator(
            self._project_folder, compute_target=self._mock_compute_target,
            inputs=[self._mock_data_ref_train])
        self.assertEqual(1, len(es.run_config.data_references))
        dref = es.run_config.data_references['traindata']
        self._validate_train_data_ref(dref)

        self._experiment.submit(es, inputs=[self._mock_data_ref_test])
        # validate original estimator
        self.assertEqual(1, len(es.run_config.data_references))
        dref = es.run_config.data_references['traindata']
        self._validate_train_data_ref(dref)

        self.assertEqual(2, len(es._last_submitted_runconfig.data_references))

        dref = es._last_submitted_runconfig.data_references['datastore']
        self._validate_test_data_ref(dref)

    @patch('azureml.train.estimator.MMLBaseEstimator._submit')
    def test_datastore_fit_override_script_params(self, mock_fit):
        script_params = {"--train": self._mock_data_ref_train}
        es = Estimator(
            self._project_folder, compute_target=self._mock_compute_target,
            script_params=script_params)
        self.assertEqual(1, len(es.run_config.data_references))
        dref = es.run_config.data_references['traindata']
        self._validate_train_data_ref(dref)

        custom_params = {"--testdata": self._mock_data_ref_test}
        self._experiment.submit(es, script_params=custom_params)
        # validate original estimator
        self.assertEqual(1, len(es.run_config.data_references))
        dref = es.run_config.data_references['traindata']
        self._validate_train_data_ref(dref)

        self.assertEqual(2, len(es._last_submitted_runconfig.data_references))

        dref = es._last_submitted_runconfig.data_references['datastore']
        self._validate_test_data_ref(dref)

    @patch('azureml.train.estimator.MMLBaseEstimator._submit')
    def test_datastore_fit_script_params_override_inputs(self, mock_fit):
        es = Estimator(
            self._project_folder, compute_target=self._mock_compute_target,
            inputs=[self._mock_data_ref_train])
        self.assertEqual(1, len(es.run_config.data_references))
        dref = es.run_config.data_references['traindata']
        self._validate_train_data_ref(dref)

        custom_params = {"--testdata": self._mock_data_ref_test}
        self._experiment.submit(es, script_params=custom_params)
        # validate original estimator
        self.assertEqual(1, len(es.run_config.data_references))
        dref = es.run_config.data_references['traindata']
        self._validate_train_data_ref(dref)

        self.assertEqual(2, len(es._last_submitted_runconfig.data_references))

        dref = es._last_submitted_runconfig.data_references['datastore']
        self._validate_test_data_ref(dref)

    @patch('azureml.train.estimator.MMLBaseEstimator._submit')
    def test_datastore_fit_inputs_override_script_params(self, mock_fit):
        script_params = {"--train": self._mock_data_ref_train}
        es = Estimator(
            self._project_folder, compute_target=self._mock_compute_target,
            script_params=script_params)
        self.assertEqual(1, len(es.run_config.data_references))
        dref = es.run_config.data_references['traindata']
        self._validate_train_data_ref(dref)

        self._experiment.submit(es, inputs=[self._mock_data_ref_test])
        # validate original estimator
        self.assertEqual(1, len(es.run_config.data_references))
        dref = es.run_config.data_references['traindata']
        self._validate_train_data_ref(dref)

        self.assertEqual(2, len(es._last_submitted_runconfig.data_references))

        dref = es._last_submitted_runconfig.data_references['datastore']
        self._validate_test_data_ref(dref)

    @patch('azureml.train.estimator.MMLBaseEstimator._submit')
    def test_datastore_fit_inputs_override_empty(self, mock_fit):
        es = Estimator(
            self._project_folder, compute_target=self._mock_compute_target)
        self.assertEqual(0, len(es.run_config.data_references))

        self._experiment.submit(es, inputs=[self._mock_data_ref_test])
        # validate original estimator
        self.assertEqual(0, len(es.run_config.data_references))

        self.assertEqual(1, len(es._last_submitted_runconfig.data_references))

        dref = es._last_submitted_runconfig.data_references['datastore']
        self._validate_test_data_ref(dref)

    @patch('azureml.train.estimator.MMLBaseEstimator._submit')
    def test_datastore_fit_script_params_override_empty(self, mock_fit):
        es = Estimator(
            self._project_folder, compute_target=self._mock_compute_target)
        self.assertEqual(0, len(es.run_config.data_references))

        custom_params = {"--testdata": self._mock_data_ref_test}
        self._experiment.submit(es, script_params=custom_params)
        # validate original estimator
        self.assertEqual(0, len(es.run_config.data_references))

        self.assertEqual(1, len(es._last_submitted_runconfig.data_references))

        dref = es._last_submitted_runconfig.data_references['datastore']
        self._validate_test_data_ref(dref)

    @patch('azureml.train.estimator.MMLBaseEstimator._submit')
    def test_datastore_fit_override_inputs_script_params(self, mock_fit):
        es = Estimator(
            self._project_folder, compute_target=self._mock_compute_target)
        self.assertEqual(0, len(es.run_config.data_references))

        custom_params = {"--testdata": self._mock_data_ref_test}
        self._experiment.submit(es, script_params=custom_params, inputs=[self._mock_data_ref_train])
        # validate original estimator
        self.assertEqual(0, len(es.run_config.data_references))

        self.assertEqual(2, len(es._last_submitted_runconfig.data_references))
        dref = es._last_submitted_runconfig.data_references['traindata']
        self._validate_train_data_ref(dref)

        dref = es._last_submitted_runconfig.data_references['datastore']
        self._validate_test_data_ref(dref)

    def _validate_train_data_ref(self, dref):
        self.assertEqual(EstimatorUnitTests.DATA_STORE_NAME, dref.data_store_name)
        self.assertEqual(EstimatorUnitTests.PATH_ON_DATA_STORE, dref.path_on_data_store)
        self.assertEqual('mount', dref.mode)

    def _validate_test_data_ref(self, dref):
        self.assertEqual(EstimatorUnitTests.DATA_STORE_NAME, dref.data_store_name)
        self.assertIsNone(dref.path_on_data_store)
        self.assertEqual('mount', dref.mode)

    def test_datastore_telemetry(self):
        print("\ntest_datastore_telemetry")
        es = Estimator(
            self._project_folder, compute_target=self._mock_compute_target,
            inputs=[self._mock_data_ref_train])

        expect = {
            "total": 1,
            "mount": 1
        }
        actual = es._get_telemetry_values(es._fit)
        self.assertEqual(True, actual['amlDataReferencesEnabled'])
        self.assertEqual(json.dumps(expect), actual['amlDataReferences'])

    def test_estimator_get_telemetry_values(self):
        est = Estimator(self._project_folder, compute_target=self._mock_compute_target,
                        entry_script='myscript.py', script_params={"arg1": 123, "arg2": "value"})
        telemetry_values = est._get_telemetry_values(est._fit)
        self.assertEqual('azureml-sdk-train', telemetry_values['amlClientType'])
        self.assertEqual(est._fit.__name__, telemetry_values['amlClientFunction'])
        self.assertEqual(est.__class__.__module__, telemetry_values['amlClientModule'])
        self.assertEqual(est.__class__.__name__, telemetry_values['amlClientClass'])
        self.assertEqual('myscript.py', telemetry_values['scriptName'])
        self.assertIn('arg1 123', telemetry_values['scriptArguments'])
        self.assertIn('arg2 value', telemetry_values['scriptArguments'])
        self.assertEqual(False, telemetry_values['useCustomDockerImage'])
        self.assertEqual(False, telemetry_values['addCondaOrPipPackage'])

    @patch('azureml.train.estimator.MMLBaseEstimator._fit')
    def test_estimator_negative(self, mock_fit):
        try:
            Estimator(self._project_folder, compute_target=self._mock_compute_target_local, node_count=2,
                      distributed_backend="mpi")
            raise Exception("Exception should be thrown but was not.")
        except Exception as ex:
            self.assertEqual('Compute target should be Batch AI for distributed training (node_count > 1).',
                             str(ex))

    def test_custom_distrib_compute(self):
        estimator = Estimator(self._project_folder, compute_target=self._mock_compute_target)
        self.assertEqual("Python", estimator._estimator_config.framework)
        self.assertEqual(DEFAULT_CPU_IMAGE, estimator._estimator_config.environment.docker.base_image)
        estimator = Estimator(self._project_folder, compute_target=self._mock_compute_target, node_count=2,
                              distributed_backend="mpi")
        self.assertEqual("PythonMpi", estimator._estimator_config.framework)
        self.assertEqual(DEFAULT_CPU_IMAGE, estimator._estimator_config.environment.docker.base_image)
        estimator = Estimator(self._project_folder, compute_target=self._mock_compute_target,
                              process_count_per_node=2, distributed_backend="mpi")
        self.assertEqual("PythonMpi", estimator._estimator_config.framework)
        self.assertEqual(DEFAULT_CPU_IMAGE, estimator._estimator_config.environment.docker.base_image)
        estimator = Estimator(self._project_folder, compute_target=self._mock_compute_target,
                              process_count_per_node=2, node_count=4, distributed_backend="mpi")
        self.assertEqual("PythonMpi", estimator._estimator_config.framework)
        self.assertEqual(DEFAULT_CPU_IMAGE, estimator._estimator_config.environment.docker.base_image)

        estimator = Estimator(self._project_folder, compute_target=self._mock_compute_target,
                              process_count_per_node=2, node_count=4, use_gpu=True, distributed_backend="mpi")
        self.assertEqual("PythonMpi", estimator._estimator_config.framework)
        self.assertEqual(DEFAULT_GPU_IMAGE, estimator._estimator_config.environment.docker.base_image)
        self.assertEqual("^docker0",
                         estimator._estimator_config.environment.environment_variables["NCCL_SOCKET_IFNAME"])

    def test_merge_pip_packages_and_requirements(self):
        requirements = ["numpy==1.6", "pandas>0.3.1", "tensorflow"]
        with open("requirements.txt", "w") as out_file:
            for requirement in requirements:
                out_file.write(requirement)
                out_file.write("\n")

        pip_packages = ["cntk", "numpy"]
        estimator = Estimator(self._project_folder, compute_target=self._mock_compute_target,
                              pip_packages=pip_packages, pip_requirements_file_path="requirements.txt")

        est_packages = list(estimator.conda_dependencies.pip_packages)
        self.assertTrue("numpy==1.6" in est_packages)
        self.assertTrue("pandas>0.3.1" in est_packages)
        self.assertTrue("tensorflow" in est_packages)
        self.assertTrue("cntk" in est_packages)

    @patch('azureml.train.estimator.MMLBaseEstimator._submit')
    @patch('azureml.core.conda_dependencies.CondaDependencies.save_to_file')
    @patch('azureml.core.runconfig.RunConfiguration.save')
    def test_fit_override_script_params(self, mock_run_config, mock_conda_dependencies, mock_submit):
        estimator = Estimator(self._project_folder, compute_target=self._mock_compute_target)
        self._experiment.submit(estimator, script_params={"param1": "value1"})
        self.assertEqual(2, len(estimator._last_submitted_runconfig.arguments))
        self.assertTrue("param1" in estimator._last_submitted_runconfig.arguments)
        self.assertTrue("value1" in estimator._last_submitted_runconfig.arguments)

        estimator = Estimator(self._project_folder, compute_target=self._mock_compute_target,
                              script_params={"param1": "value1"})
        self._experiment.submit(estimator, script_params={"param2": "value2"})
        self.assertEqual(4, len(estimator._last_submitted_runconfig.arguments))
        self.assertTrue("param1" in estimator._last_submitted_runconfig.arguments)
        self.assertTrue("value1" in estimator._last_submitted_runconfig.arguments)
        self.assertTrue("param2" in estimator._last_submitted_runconfig.arguments)
        self.assertTrue("value2" in estimator._last_submitted_runconfig.arguments)


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner())
