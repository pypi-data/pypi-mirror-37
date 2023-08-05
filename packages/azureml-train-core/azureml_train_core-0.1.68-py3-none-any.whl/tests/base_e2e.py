import os
from os import path
import shutil
import sys
from azureml.core.workspace import Workspace
from azureml.core.compute.batchai import BatchAiCompute
from azureml.core.compute_target import BatchAITarget, LocalTarget
from azureml.core.compute import RemoteCompute
from azureml.core.experiment import Experiment


class BaseE2E:
    _SUBSCRIPTION_ID = "c422cbf2-d107-4b13-a514-08b0e5f93a02"
    _RESOURCE_GROUP = "AmlTrainCoreTest"
    _SERVICE_PRINCIPAL_ID = "e35635bb-2d8d-4bb1-835e-387b91bd794d"
    _TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47"
    _STORAGE_ACCOUNT = 'trainingserviceeastus'
    _KEYVAULT = 'vienna-train-core'
    _DATA_STORAGE_KEY = 'DataStoreTestKey'
    _BLOB_CONTAINER = 'batchai'
    _TRAIN_FILE_NAME = "Train-28x28_cntk_text.txt"
    _TEST_FILE_NAME = "Test-28x28_cntk_text.txt"
    _DATA_STORE_NAME = "mnist_test"

    @staticmethod
    def _az_login():
        curdir = path.dirname(path.abspath(__file__))
        sys.path.append(path.join(curdir, "../../../scripts"))

        import az_utils
        from utils import run_command

        secret_key = az_utils.get_secret_from_common_keyvault(BaseE2E._SERVICE_PRINCIPAL_ID)
        run_command(["az", "login", "--service-principal", "-u", BaseE2E._SERVICE_PRINCIPAL_ID, "-p",
                     secret_key, "-t", BaseE2E._TENANT_ID], shell=True, stream_stdout=False, return_stdout=True)

        az_utils.set_account(BaseE2E._SUBSCRIPTION_ID)

    @staticmethod
    def get_workspace(workspace_name):
        return Workspace._get_or_create(workspace_name,
                                        subscription_id=BaseE2E._SUBSCRIPTION_ID,
                                        resource_group=BaseE2E._RESOURCE_GROUP)

    @staticmethod
    def create_project(project_name):
        print("Creating the Project...")
        cur_dir = path.dirname(path.abspath(__file__))
        os.mkdir(path.join(cur_dir, project_name))
        print("Project created successfully...")

    @staticmethod
    def copy_user_script_to_project(project_name, script_name):
        print("Copying user script to the Project...")
        cur_dir = path.dirname(path.abspath(__file__))
        shutil.copy(path.join(cur_dir, script_name), path.join(cur_dir, project_name))

    @staticmethod
    def create_batchai_compute_target(workspace, name):
        batchai_configuration = BatchAiCompute.provisioning_configuration(
            vm_size="Standard_NC6",
            autoscale_enabled=True,
            autoscale_min_nodes=0,
            autoscale_max_nodes=2)

        batchai_compute = BatchAiCompute.create(workspace,
                                                name,
                                                batchai_configuration)
        batchai_compute.wait_for_completion(show_output=True)
        return batchai_compute

    @staticmethod
    def get_dsvm_target(workspace):
        return RemoteCompute.attach(workspace, "testdsvm", username="amltraincoretest",
                                    address="104.209.192.172", ssh_port=22, password="AmlTrainCore1#")

    @staticmethod
    def get_batchai_compute(workspace, name):
        return BatchAiCompute(workspace, name)

    @staticmethod
    def get_batchai_target(name):
        return BatchAITarget(name,
                             subscription_id=BaseE2E._SUBSCRIPTION_ID,
                             resource_group_name=BaseE2E._RESOURCE_GROUP,
                             cluster_name=name)

    @staticmethod
    def get_local_target():
        return LocalTarget()

    @staticmethod
    def run_experiment(estimator, workspace, experiment_name):
        print("Submitting the user experiment...")
        experiment = Experiment(workspace, experiment_name)
        experiment_run = experiment.submit(estimator)

        print("Waiting for the experiment to get finished...")
        experiment_run.wait_for_completion(show_output=True, wait_post_processing=True)
        print("Experiment finished with status...")
        print(experiment_run.get_details())
        return experiment_run

    @staticmethod
    def cleanup_run(experiment_run):
        print("Cleaning up the resources...")
        print("Clean up the experiment...")
        if experiment_run:
            experiment_run.clean()

    @staticmethod
    def cleanup_project(project_name, workspace):
        cur_dir = path.dirname(path.abspath(__file__))
        if path.exists(path.join(cur_dir, project_name)):

            print("Try to remove the directory {}".format(path.join(cur_dir, project_name)))
            shutil.rmtree(path.join(cur_dir, project_name))
            print("Project deleted successfully...")

    @staticmethod
    def cleanup(experiment_run, project_name, workspace):
        BaseE2E.cleanup_run(experiment_run)
        BaseE2E.cleanup_project(project_name, workspace)

    @staticmethod
    def setup_datastore(workspace):
        curdir = path.dirname(path.abspath(__file__))
        sys.path.append(path.join(curdir, "../../../scripts"))

        from az_utils import get_secret_from_keyvault
        from azureml.data.datastore_client import _DatastoreClient

        def log_creating_store(name, workspace):
            print("Creating datastore: '{}' in sid: {}, rg: {}, ws: {}".format(
                name,
                workspace.subscription_id,
                workspace.resource_group,
                workspace.name
            ))

        account_key = get_secret_from_keyvault(BaseE2E._KEYVAULT, BaseE2E._DATA_STORAGE_KEY)

        log_creating_store(BaseE2E._DATA_STORE_NAME, workspace)
        # TODO: remove get in the future
        try:
            datastore = _DatastoreClient.get(workspace, BaseE2E._DATA_STORE_NAME)
        except Exception:
            datastore = _DatastoreClient.register_azure_blob_container(
                workspace, BaseE2E._DATA_STORE_NAME, BaseE2E._BLOB_CONTAINER,
                BaseE2E._STORAGE_ACCOUNT, account_key=account_key)

        return datastore
