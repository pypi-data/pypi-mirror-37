import unittest
import xmlrunner
import time

from base_e2e import BaseE2E
from azureml.train.dnn import TensorFlow


class TFE2ETests(unittest.TestCase):
    _WORKSPACE_NAME = "traincore-gated"

    def setUp(self):
        self._workspace = BaseE2E.get_workspace(self._WORKSPACE_NAME)

    # This test fails with: Error copying files to the remote target.
    # Check that you have read, write, and execute permission
    # to /tmp on the target, and that the disk is not full.
    # Disabling to unblock.
    '''
    def test_dsvm_workflow(self):
        project_name = "test_tf_project" + str(int(time.time()))
        try:
            project = BaseE2E.create_project(self._workspace, project_name)
        except Exception as ex:
            BaseE2E.cleanup_project(project)
            raise ex

        dsvm_compute_target = BaseE2E.get_dsvm_target()
        project.attach_legacy_compute_target(dsvm_compute_target)

        BaseE2E.copy_user_script_to_project(project, "tf_mnist.py")

        print("Creating TensorFlow Estimator...")
        tf_estimator = TensorFlow(project, compute_target=dsvm_compute_target, node_count=1, use_mpi=False,
                                  entry_script="tf_mnist.py")

        try:
            experiment_run = BaseE2E.run_experiment(tf_estimator)
            run_status = experiment_run.get_status()
            assert run_status["status"] == "Completed"
        finally:
            BaseE2E.cleanup(experiment_run, project)
    '''

    def test_batchai_workflow(self):
        project_name = "test_tf_project" + str(int(time.time()))
        try:
            BaseE2E.create_project(project_name)
        except Exception:
            BaseE2E.cleanup_project(project_name)
            raise

        batchai_compute_name = "train_gated_d3"
        batchai_compute_target = BaseE2E.get_batchai_compute(self._workspace, batchai_compute_name)

        BaseE2E.copy_user_script_to_project(project_name, "tf_mnist.py")

        print("Creating TensorFlow Estimator...")
        tf_estimator = TensorFlow(project_name,
                                  compute_target=batchai_compute_target,
                                  node_count=1, use_mpi=False,
                                  entry_script="tf_mnist.py")

        experiment_run = None
        try:
            experiment_run = BaseE2E.run_experiment(tf_estimator, self._workspace, "tf_e2e_test")
            run_status = experiment_run.get_status()
            assert run_status == "Completed"
        finally:
            BaseE2E.cleanup(experiment_run, project_name, self._workspace)


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner())
