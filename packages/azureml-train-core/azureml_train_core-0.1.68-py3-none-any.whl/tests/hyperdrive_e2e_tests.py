import unittest
import xmlrunner
import time

from base_e2e import BaseE2E
from azureml.train.dnn import TensorFlow
from azureml.train.hyperdrive import RandomParameterSampling,\
    uniform, BanditPolicy, HyperDriveRunConfig, PrimaryMetricGoal
from azureml.core.experiment import Experiment


class HyperDriveE2ETests(unittest.TestCase):
    _WORKSPACE_NAME = "traincore-gated"

    def setUp(self):
        self._workspace = BaseE2E.get_workspace(self._WORKSPACE_NAME)

    def test_batchai_workflow(self):
        project_name = "test_hd_project" + str(int(time.time()))
        try:
            BaseE2E.create_project(project_name)
        except Exception:
            BaseE2E.cleanup_project(project_name)
            raise

        batchai_compute_name = "train_gated_d3"
        batchai_compute_target = BaseE2E.get_batchai_compute(self._workspace, batchai_compute_name)

        BaseE2E.copy_user_script_to_project(project_name, "tf_mnist.py")

        print("Creating TensorFlow Estimator...")
        tf_estimator = TensorFlow(project_name, node_count=1, compute_target=batchai_compute_target,
                                  entry_script="tf_mnist.py")

        param_sampling = RandomParameterSampling(
            {
                "learning_rate": uniform(0.1, 0.2),
            })

        early_termination_policy = BanditPolicy(slack_factor=0.1, evaluation_interval=1)

        hyperdrive_run_config = HyperDriveRunConfig(estimator=tf_estimator,
                                                    hyperparameter_sampling=param_sampling,
                                                    policy=early_termination_policy,
                                                    primary_metric_name="Loss",
                                                    primary_metric_goal=PrimaryMetricGoal.MINIMIZE,
                                                    max_total_runs=1,
                                                    max_concurrent_runs=1,
                                                    compute_target=batchai_compute_target)

        print("Submitting the hyperdrive experiment...")
        experiment = Experiment(self._workspace, project_name)
        hyperdrive_run = experiment.submit(hyperdrive_run_config)

        print("Waiting for the experiment to get finished...")
        hyperdrive_run.wait_for_completion(show_output=True)
        experiment_status = hyperdrive_run.get_details()

        print("Experiment finished with status...")
        print(experiment_status)

        print("Cleaning up the resources...")
        BaseE2E.cleanup_project(project_name, self._workspace)

        assert experiment_status["status"] == "Completed"


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner())
