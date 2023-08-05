# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root
# for full license information.
# ==============================================================================

import unittest

from azureml.exceptions import AzureMLException
from mock import patch
from mock_objects import MockObjects
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import DEFAULT_CPU_IMAGE
import azureml.train.restclients.hyperdrive as HyperDriveClient
from azureml.train.hyperdrive.runconfig import HyperDriveRunConfig
from azureml.train.hyperdrive.sampling import RandomParameterSampling, BayesianParameterSampling, GridParameterSampling
from azureml.train.hyperdrive.policy import BanditPolicy, MedianStoppingPolicy, TruncationSelectionPolicy
from azureml.train.hyperdrive.parameter_expressions import uniform, choice, quniform, randint
from azureml.train.hyperdrive.run import HyperDriveRun, PrimaryMetricGoal
from azureml.train.hyperdrive._search import search, _get_telemetry_values
from azureml._base_sdk_common.common import AML_CONFIG_DIR, COMPUTECONTEXT_EXTENSION
import os
import shutil
import json


class HyperDriveUnitTests(unittest.TestCase):

    def setUp(self):
        self._mock_estimator = MockObjects.get_estimator()
        self._mock_workspace = MockObjects.get_workspace()
        self._mock_compute_target = MockObjects.get_compute_target_batchai()
        config_dir = os.path.join(
            self._mock_estimator.source_directory, AML_CONFIG_DIR)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        compute_file_path = os.path.join(
            config_dir, self._mock_compute_target.name + COMPUTECONTEXT_EXTENSION)
        with open(compute_file_path, "w") as computefile:
            computefile.write(json.dumps(
                self._mock_compute_target._serialize_to_dict()))
        self.maxDiff = None

    def tearDown(self):
        config_dir = os.path.join(
            self._mock_estimator.source_directory, AML_CONFIG_DIR)
        if os.path.exists(config_dir):
            shutil.rmtree(config_dir)

    @staticmethod
    def _get_hyperdrive_run_config(estimator=None,
                                   parameter_sampling=None,
                                   no_policy=False,
                                   no_policy_param=False,
                                   primary_metric_goal=PrimaryMetricGoal.MAXIMIZE):

        default_sampling = RandomParameterSampling(
            {
                "learning_rate": uniform(0.01, 0.001),
                "batch_size": choice(128, 256)
            })

        param_sampling = default_sampling if parameter_sampling is None else parameter_sampling
        estimator = MockObjects.get_estimator() if estimator is None else estimator

        if no_policy_param:
            return HyperDriveRunConfig(estimator=estimator,
                                       hyperparameter_sampling=param_sampling,
                                       primary_metric_name="test_metric",
                                       primary_metric_goal=primary_metric_goal,
                                       max_total_runs=100,
                                       max_concurrent_runs=15)
        else:
            policy = None if no_policy else BanditPolicy(slack_factor=0.2, evaluation_interval=100)
            return HyperDriveRunConfig(estimator=estimator,
                                       hyperparameter_sampling=param_sampling,
                                       policy=policy,
                                       primary_metric_name="test_metric",
                                       primary_metric_goal=primary_metric_goal,
                                       max_total_runs=100,
                                       max_concurrent_runs=15)

    @patch("azureml._base_sdk_common.service_discovery.ServiceDiscovery.get_service_url")
    def test_hyperdrive_config(self, mock_url):
        mock_url.return_value = "http://test-end-point"
        run_config = self._get_hyperdrive_run_config()
        assert run_config._primary_metric_config["name"] == "test_metric"
        assert run_config._primary_metric_config["goal"] == "maximize"
        self.assertEqual(run_config._get_platform_config(self._mock_workspace, "hd_unittest")["Definition"],
                         self.get_expected_run_config()
                         ["platform_config"]["Definition"],
                         msg="Platform config definition doesn't match.")

    @patch("azureml._base_sdk_common.service_discovery.ServiceDiscovery.get_service_url")
    def test_hyperdrive_config_conda_deps(self, mock_url):
        conda_deps = CondaDependencies()
        mock_url.return_value = "http://test-end-point"
        run_config = self._get_hyperdrive_run_config(estimator=MockObjects.get_estimator_with_conda_dependencies())
        self.assertEqual(run_config._get_platform_config(self._mock_workspace, "hd_unittest")
                         ["Definition"]["Overrides"]['environment']['python']
                         ['condaDependencies'],
                         conda_deps._conda_dependencies,
                         msg="Conda dependencies object in run config doesn't match.")

    @patch("azureml._base_sdk_common.service_discovery.ServiceDiscovery.get_service_url")
    def test_hyperdrive_config_no_policy(self, mock_url):
        mock_url.return_value = "http://test-end-point"

        expected_policy = {'name': 'MedianStopping',
                           'properties': {'delay_evaluation': 5, 'evaluation_interval': 1}}
        run_config = self._get_hyperdrive_run_config(no_policy=True)
        self.assertEqual(run_config._policy_config,
                         expected_policy,
                         msg="Default policy config doesn't match.")
        run_config = self._get_hyperdrive_run_config(no_policy_param=True)
        self.assertEqual(run_config._policy_config,
                         expected_policy,
                         msg="Default policy config doesn't match.")

    @patch("azureml._base_sdk_common.service_discovery.ServiceDiscovery.get_service_url")
    def test_create_exp_config(self, mock_url):
        mock_url.return_value = "http://test-end-point"
        run_config = self._get_hyperdrive_run_config()

        experiment = HyperDriveClient.CreateExperimentDto(generator_config=run_config._generator_config,
                                                          max_concurrent_jobs=run_config._max_concurrent_runs,
                                                          max_total_jobs=run_config._max_total_runs,
                                                          max_duration_minutes=run_config._max_duration_minutes,
                                                          platform=run_config._platform,
                                                          platform_config=run_config.
                                                          _get_platform_config(self._mock_workspace, "test_project"),
                                                          policy_config=run_config._policy_config,
                                                          primary_metric_config=run_config._primary_metric_config,
                                                          user="sukaruna@microsoft.com", name="test_run")

        self.assertEqual(experiment.to_dict(),
                         self.get_expected_run_config(),
                         msg="Config from create experiment is different from expected config.")

    @patch("azureml.core.script_run.ScriptRun.__init__")
    @patch("azureml.core.run.Run.get_children")
    @patch("azureml.train.hyperdrive.HyperDriveRun.get_metrics")
    @patch("azureml._base_sdk_common.service_discovery.ServiceDiscovery.get_service_url")
    def test_get_best_run_single_metric(self, mock_url, mock_metrics, mock_children, mock_exp_run):
        mock_url.return_value = "http://test-end-point"
        hyperdrive_run = HyperDriveRun(MockObjects.get_experiment(), "123",
                                       MockObjects.get_run_config(), self._get_hyperdrive_run_config())

        mock_exp_run.return_value = None
        run_1 = MockObjects.get_run("1", {'test_metric': 0.6792452830188679, 'Regularization_rate': 0.10151940173504})
        run_2 = MockObjects.get_run("2", {'test_metric': 0.6981132075471698,
                                          'Regularization_rate': 0.0496075020981801})
        mock_children.return_value = [run_1, run_2]

        run_metrics = {}
        run_metrics["1"] = {'test_metric': 0.6792452830188679,
                            'Regularization_rate': 0.10151940173504}
        run_metrics["2"] = {'test_metric': 0.6981132075471698,
                            'Regularization_rate': 0.0496075020981801}
        mock_metrics.return_value = run_metrics

        best_run = hyperdrive_run._get_best_run_id_by_primary_metric()
        self.assertEqual(best_run, "2", "Best run id doesn't match  for single metric and maximize.")

        hyperdrive_run = HyperDriveRun(MockObjects.get_experiment(),
                                       "123",
                                       MockObjects.get_run_config(),
                                       self._get_hyperdrive_run_config(primary_metric_goal=PrimaryMetricGoal.MINIMIZE))
        best_run = hyperdrive_run._get_best_run_id_by_primary_metric()
        self.assertEqual(best_run, "1", "Best run id doesn't match for single metric and minimize.")

    @patch("azureml.core.script_run.ScriptRun.__init__")
    @patch("azureml.core.run.Run.get_children")
    @patch("azureml.train.hyperdrive.HyperDriveRun.get_metrics")
    @patch("azureml._base_sdk_common.service_discovery.ServiceDiscovery.get_service_url")
    def test_get_best_run_array_metric(self, mock_url, mock_metrics, mock_children, mock_exp_run):
        mock_url.return_value = "http://test-end-point"
        hyperdrive_run = HyperDriveRun(MockObjects.get_experiment(), "123",
                                       MockObjects.get_run_config(), self._get_hyperdrive_run_config())

        mock_exp_run.return_value = None
        run_1 = MockObjects.get_run("1", {"test_metric": [0.6792452830188679, 0.10151940173504],
                                          "Regularization_rate": 0.10151940173504})
        run_2 = MockObjects.get_run("2", {"test_metric": [0.6981132075471698, 0.0496075020981801],
                                          "Regularization_rate": 0.0496075020981801})
        mock_children.return_value = [run_1, run_2]

        run_metrics = {}
        run_metrics["1"] = {'test_metric': [0.6792452830188679, 0.10151940173504],
                            'Regularization_rate': 0.10151940173504}
        run_metrics["2"] = {'test_metric': [0.6981132075471698, 0.0496075020981801],
                            'Regularization_rate': 0.0496075020981801}
        mock_metrics.return_value = run_metrics
        best_run = hyperdrive_run._get_best_run_id_by_primary_metric()
        self.assertEqual(best_run, "2", "Best run id doesn't match  for array metric and maximize.")

        hyperdrive_run = HyperDriveRun(MockObjects.get_experiment(),
                                       "123",
                                       MockObjects.get_run_config(),
                                       self._get_hyperdrive_run_config(primary_metric_goal=PrimaryMetricGoal.MINIMIZE))
        best_run = hyperdrive_run._get_best_run_id_by_primary_metric()
        self.assertEqual(best_run, "2", "Best run id doesn't match for array metric and minimize.")

    @patch("azureml.core.script_run.ScriptRun.__init__")
    @patch("azureml.core.run.Run.get_children")
    @patch("azureml.train.hyperdrive.HyperDriveRun.get_metrics")
    @patch("azureml._base_sdk_common.service_discovery.ServiceDiscovery.get_service_url")
    def test_get_best_run_empty_metric(self, mock_url, mock_metrics, mock_children, mock_exp_run):
        mock_url.return_value = "http://test-end-point"
        hyperdrive_run = HyperDriveRun(MockObjects.get_experiment(), "123",
                                       MockObjects.get_run_config(), self._get_hyperdrive_run_config())

        mock_exp_run.return_value = None
        run_1 = MockObjects.get_run("1", {})
        mock_children.return_value = [run_1]

        run_metrics = {"1": {}}
        mock_metrics.return_value = run_metrics
        best_run = hyperdrive_run._get_best_run_id_by_primary_metric()
        self.assertIsNone(best_run, "Best run for empty metrics is not none.")

    @patch("azureml.core.script_run.ScriptRun.__init__")
    @patch("azureml.core.run.Run.get_children")
    @patch("azureml.train.hyperdrive.HyperDriveRun.get_metrics")
    @patch("azureml._base_sdk_common.service_discovery.ServiceDiscovery.get_service_url")
    def test_get_best_run_partial_metric(self, mock_url, mock_metrics, mock_children, mock_exp_run):
        mock_url.return_value = "http://test-end-point"
        hyperdrive_run = HyperDriveRun(MockObjects.get_experiment(), "123",
                                       MockObjects.get_run_config(), self._get_hyperdrive_run_config())

        mock_exp_run.return_value = None
        run_1 = MockObjects.get_run("1", {"Regularization_rate": 0.10151940173504})
        mock_children.return_value = [run_1]

        run_metrics = {"1": {'xxx': 0.10151940173504}}
        mock_metrics.return_value = run_metrics
        best_run = hyperdrive_run._get_best_run_id_by_primary_metric()
        self.assertIsNone(best_run, "Best run for partial metric logging is not None.")

    @patch("azureml._base_sdk_common.service_discovery.ServiceDiscovery.get_service_url")
    def test_remove_duplicate_arguments_duplicates(self, mock_url):
        mock_url.return_value = "http://test-end-point"
        # Case0: Estimator has no arguments
        hyperdrive_run_config = self._get_hyperdrive_run_config()
        estimator_args = MockObjects.get_estimator().run_config.arguments
        new_estimator_run_config = hyperdrive_run_config._remove_duplicate_estimator_arguments()
        self.assertEqual(estimator_args, [])
        self.assertEqual(new_estimator_run_config.arguments, [])
        self.assertEqual(hyperdrive_run_config._generator_config, {
            'parameter_space': {
                'batch_size': ['choice', [[128, 256]]],
                'learning_rate': ['uniform', [0.01, 0.001]]
            },
            'name': 'RANDOM'
        })

        # Case1: Both estimator and hyperdrive have arguments but no overlap
        estimator = MockObjects.get_estimator(["--arg1", "val1"])
        hyperdrive_run_config = self._get_hyperdrive_run_config(estimator=estimator)
        new_estimator_run_config = hyperdrive_run_config._remove_duplicate_estimator_arguments()
        self.assertEqual(new_estimator_run_config.arguments, ["--arg1", "val1"])
        self.assertEqual(estimator.run_config.arguments, ["--arg1", "val1"])
        self.assertEqual(hyperdrive_run_config._generator_config, {
            'parameter_space': {
                'batch_size': ['choice', [[128, 256]]],
                'learning_rate': ['uniform', [0.01, 0.001]]
            },
            'name': 'RANDOM'
        })

        # Case2: There are duplicates with hyphen mismatch (estimator has added hyphen)
        estimator = MockObjects.get_estimator(["--batch_size", "150"])
        hyperdrive_run_config = self._get_hyperdrive_run_config(estimator=estimator)
        new_estimator_run_config = hyperdrive_run_config._remove_duplicate_estimator_arguments()
        self.assertEqual(estimator.run_config.arguments, ["--batch_size", "150"])
        self.assertEqual(new_estimator_run_config.arguments, [])
        self.assertEqual(hyperdrive_run_config._generator_config, {
            'parameter_space': {
                'batch_size': ['choice', [[128, 256]]],
                'learning_rate': ['uniform', [0.01, 0.001]]
            },
            'name': 'RANDOM'
        })

        # Case3: Exact duplicates
        estimator = MockObjects.get_estimator(["batch_size", "150"])
        hyperdrive_run_config = self._get_hyperdrive_run_config(estimator=estimator)
        new_estimator_run_config = hyperdrive_run_config._remove_duplicate_estimator_arguments()
        self.assertEqual(estimator.run_config.arguments, ["batch_size", "150"])
        self.assertEqual(new_estimator_run_config.arguments, [])
        self.assertEqual(hyperdrive_run_config._generator_config, {
            'parameter_space': {
                'batch_size': ['choice', [[128, 256]]],
                'learning_rate': ['uniform', [0.01, 0.001]]
            },
            'name': 'RANDOM'
        })

        # Case4: Exact duplicates and zero input param value
        estimator = MockObjects.get_estimator(['--data-dir', '$AZUREML_DATAREFERENCE_workspacefilestore',
                                               '--network-name', 'vgg16', '--num-epochs', 200,
                                               '--minibatch-size', 32, '--learning-rate', 0.001,
                                               '--momentum', 0.9, '--step-size', 7, '--gamma', 0.9,
                                               '--num-dataload-workers', 6, '--epochs-before-unfreeze-all', 0,
                                               '--checkpoint-epochs', 50])
        param_sampling = RandomParameterSampling({
            '--network-name': choice('densenet201', 'resnet152', 'alexnet', 'vgg19_bn'),
            '--minibatch-size': choice(8, 16),
            '--learning-rate': uniform(0.00001, 0.001),
            '--step-size': choice(10, 25, 50),
            '--gamma': uniform(0.7, 0.99),
            '--optimizer-type': choice('sgd', 'adam')
        })

        hyperdrive_run_config = self._get_hyperdrive_run_config(estimator=estimator,
                                                                parameter_sampling=param_sampling)
        new_estimator_run_config = hyperdrive_run_config._remove_duplicate_estimator_arguments()
        self.assertEqual(estimator.run_config.arguments, ['--data-dir', '$AZUREML_DATAREFERENCE_workspacefilestore',
                                                          '--network-name', 'vgg16', '--num-epochs', 200,
                                                          '--minibatch-size', 32, '--learning-rate', 0.001,
                                                          '--momentum', 0.9, '--step-size', 7, '--gamma', 0.9,
                                                          '--num-dataload-workers', 6, '--epochs-before-unfreeze-all',
                                                          0, '--checkpoint-epochs', 50])
        self.assertEqual(new_estimator_run_config.arguments, ['--data-dir',
                                                              '$AZUREML_DATAREFERENCE_workspacefilestore',
                                                              '--num-epochs', 200, '--momentum', 0.9,
                                                              '--num-dataload-workers', 6,
                                                              '--epochs-before-unfreeze-all', 0,
                                                              '--checkpoint-epochs', 50])

    def test_choice_param_expression(self):
        self.assertEqual(choice(1, 4, 5), ["choice", [[1, 4, 5]]])
        self.assertEqual(choice([1, 4, 5]), ["choice", [[1, 4, 5]]])
        self.assertEqual(choice(range(1, 5)), ["choice", [[1, 2, 3, 4]]])

    def test_bandit_slack_amount(self):
        policy = BanditPolicy(slack_factor=0.1, evaluation_interval=10)
        self.assertEqual(policy.to_json()["properties"], {'delay_evaluation': 0, 'evaluation_interval': 10,
                                                          'slack_factor': 0.1})

        policy = BanditPolicy(slack_amount=0.1, evaluation_interval=10)
        self.assertEqual(policy.to_json()["properties"], {'delay_evaluation': 0, 'evaluation_interval': 10,
                                                          'slack_amount': 0.1})

    def test_medianstopping_properties(self):
        policy = MedianStoppingPolicy()
        policy_json = policy.to_json()
        self.assertEqual("MedianStopping", policy_json["name"])
        self.assertEqual({'delay_evaluation': 0, 'evaluation_interval': 1}, policy_json["properties"])

        policy = MedianStoppingPolicy(evaluation_interval=2, delay_evaluation=7)
        policy_json = policy.to_json()
        self.assertEqual("MedianStopping", policy_json["name"])
        self.assertEqual({'delay_evaluation': 7, 'evaluation_interval': 2}, policy_json["properties"])

    def test_truncationselection_properties(self):
        policy = TruncationSelectionPolicy(truncation_percentage=10)
        policy_json = policy.to_json()
        self.assertEqual("TruncationSelection", policy_json["name"])
        self.assertEqual({'delay_evaluation': 0, 'evaluation_interval': 1,
                          'exclude_finished_jobs': False, 'truncation_percentage': 10},
                         policy_json["properties"])

        policy = TruncationSelectionPolicy(evaluation_interval=2, delay_evaluation=7, truncation_percentage=5)
        policy_json = policy.to_json()
        self.assertEqual("TruncationSelection", policy_json["name"])
        self.assertEqual({'delay_evaluation': 7, 'evaluation_interval': 2,
                          'exclude_finished_jobs': False, 'truncation_percentage': 5},
                         policy_json["properties"])

    def test_bayesian_validation(self):
        parameter_space = {
            'batch_size': choice(128, 256),
            'learning_rate': uniform(0.01, 0.001),
            'layers': quniform(10, 300, 1)
        }
        sampling = BayesianParameterSampling(parameter_space)
        self.assertEqual("BayesianOptimization", sampling.to_json()["name"])

        parameter_space = {
            'batch_size': choice(128, 256),
            'learning_rate': randint(15),
            'layers': quniform(10, 300, 1)
        }

        def create_bayesian():
            BayesianParameterSampling(parameter_space)

        self.assertRaises(AzureMLException, create_bayesian)

    def test_grid_sampling_validation(self):
        parameter_space = {
            'batch_size': choice(128, 256),
            'learning_rate': choice(10, 300, 1),
            'layers': choice(10, 300, 1)
        }
        sampling = GridParameterSampling(parameter_space)
        self.assertEqual("GRID", sampling.to_json()["name"])

        parameter_space = {
            'batch_size': choice(128, 256),
            'learning_rate': randint(15),
            'layers': quniform(10, 300, 1)
        }

        def create_grid():
            GridParameterSampling(parameter_space)

        self.assertRaises(AzureMLException, create_grid)

    def test_random_sampling_validation(self):
        parameter_space = {
            'batch_size': choice(128, 256),
            'learning_rate': randint(15),
            'layers': quniform(10, 300, 1)
        }
        sampling = RandomParameterSampling(parameter_space)
        self.assertEqual("RANDOM", sampling.to_json()["name"])

    @staticmethod
    def get_expected_run_config():
        return {
            'max_duration_minutes': 10080,
            'policy_config': {
                'properties': {
                    'evaluation_interval': 100,
                    'slack_factor': 0.2,
                    'delay_evaluation': 0
                },
                'name': 'Bandit'
            },
            'study_id': None,
            'description': None,
            'generator_config': {
                'parameter_space': {
                    'batch_size': ['choice', [[128, 256]]],
                    'learning_rate': ['uniform', [0.01, 0.001]]
                },
                'name': 'RANDOM'
            },
            'platform': 'AML',
            'name': 'test_run',
            'platform_config': {
                'ResourceGroupName': 'test_rg',
                'ServiceAddress': 'http://test-end-point',
                'ServiceArmScope': 'subscriptions/test_subscription_123/'
                    'resourceGroups/test_rg/providers/'
                    'Microsoft.MachineLearningServices/'
                    'workspaces/test_ws/experiments/test_project',
                'SubscriptionId': 'test_subscription_123',
                'WorkspaceName': 'test_ws',
                'ExperimentName': 'test_project',
                'Definition': {
                    'TargetDetails': {
                        'type': 'batchai',
                        'subscription_id': 'test_subscription_123',
                        'cluster_name': 'test_cluster',
                        'resource_group_name': 'test_rg'
                    },
                    'Overrides': {
                        'spark': {
                            'configuration': {
                                'spark.app.name': 'Azure ML Experiment',
                                'spark.yarn.maxAppAttempts': 1
                            }
                        },
                        'hdi': {
                            'yarnDeployMode': 'cluster'
                        },
                        'containerInstance': {
                            'memoryGb': 4,
                            'cpuCores': 1,
                            'region': None
                        },
                        'dataReferences': {},
                        'target': 'batchai',
                        'autoPrepareEnvironment': True,
                        'environment': {
                            'docker': {
                                'arguments': [],
                                'sharedVolumes': True,
                                'enabled': False,
                                'gpuSupport': False,
                                'baseImageRegistry': {
                                    'username': None,
                                    'password': None,
                                    'address': None
                                },
                                'baseImage': DEFAULT_CPU_IMAGE
                            },
                            'spark': {
                                'packages': [
                                    {
                                        'artifact': 'mmlspark_2.11',
                                        'group': 'com.microsoft.ml.spark',
                                        'version': '0.12'
                                    }],
                                'precachePackages': True,
                                'repositories': [
                                    'https://mmlspark.azureedge.net/maven']},
                            'python': {
                                'userManagedDependencies': False,
                                'condaDependencies': {
                                    'dependencies': [
                                        'python=3.6.2',
                                        {
                                            'pip': [
                                                'azureml-defaults'
                                            ]
                                        }
                                    ],
                                    'name': 'project_environment'
                                },
                                'interpreterPath': 'python'
                            },
                            'environmentVariables': {
                                'EXAMPLE_ENV_VAR': 'EXAMPLE_VALUE'
                            }
                        },
                        'maxRunDurationSeconds': None,
                        'mpi': {'processCountPerNode': 1},
                        'framework': 'CNTK',
                        'batchai': {'nodeCount': 1},
                        'tensorflow': {'parameterServerCount': 1, 'workerCount': 1},
                        'history': {'outputCollection': True,
                                    'snapshotProject': True},
                        'script': 'testscript.py',
                        'arguments': []
                    }
                }
            },
            'user': 'sukaruna@microsoft.com',
            'primary_metric_config': {'goal': 'maximize', 'name': 'test_metric'},
            'max_total_jobs': 100,
            'max_concurrent_jobs': 15
        }

    @patch("azureml._base_sdk_common.service_discovery.ServiceDiscovery.get_service_url")
    def test_get_telemetry_values(self, mock_url):
        mock_url.return_value = "http://test-end-point"
        config = self._get_hyperdrive_run_config()
        telemetry_values = _get_telemetry_values(config, self._mock_workspace)
        self.assertEqual('azureml-sdk-train', telemetry_values['amlClientType'])
        self.assertEqual(search.__name__, telemetry_values['amlClientFunction'])
        self.assertEqual(search.__module__, telemetry_values['amlClientModule'])
        self.assertEqual('test_subscription_123', telemetry_values['subscriptionId'])
        self.assertEqual(config.estimator.__class__.__name__, telemetry_values['estimator'])
        self.assertEqual('RANDOM', telemetry_values['samplingMethod'])
        self.assertEqual('Bandit', telemetry_values['terminationPolicy'])
        self.assertEqual('maximize', telemetry_values['primaryMetricGoal'])
        self.assertEqual(100, telemetry_values['maxTotalRuns'])
        self.assertEqual(15, telemetry_values['maxConcurrentRuns'])
        self.assertEqual(10080, telemetry_values['maxDurationMinutes'])
        self.assertEqual('batchai', telemetry_values['computeTarget'])


if __name__ == "__main__":
    unittest.main()
