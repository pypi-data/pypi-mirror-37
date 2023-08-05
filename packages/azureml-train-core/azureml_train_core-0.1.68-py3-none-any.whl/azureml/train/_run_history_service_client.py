# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""_RunHistoryServiceClient exposes methods for fetching Run History data."""
from azureml._base_sdk_common.user_agent import get_user_agent
from azureml._base_sdk_common import _ClientSessionId
from azureml._restclient import RunHistoryClient
from azureml._async import WorkerPool
from azureml.core.run import Run


class _RunHistoryServiceClient(object):
    """_RunHistoryServiceClient exposes methods for fetching Run History data.

    It transforms some of the data as required by the widgets ui.
    """

    def __init__(self, experiment, custom_headers=None):
        """Initialize the _RunHistoryServiceClient object.

        :param experiment: The experiment object.
        :type experiment: azureml.core.experiment.Experiment
        :param custom_headers: Additional headers sent in the request.
        :type custom_headers: dict
        """
        self._pool = WorkerPool()
        self.service_facade = RunHistoryClient.create(workspace=experiment.workspace,
                                                      experiment_name=experiment.name,
                                                      workerpool=self._pool)

        custom_headers = custom_headers or {}
        self._common_headers = {}
        self._common_headers['x-ms-client-session-id'] = _ClientSessionId
        self._common_headers['User-Agent'] = get_user_agent()
        self._common_headers.update(custom_headers)

    @staticmethod
    def batches(list, size):
        """Convert a list into batches of the specified size.

        :param list: The list of items to split into batches.
        :type list: list
        :param size: The number of items in each batch.
        :type size: int
        """
        for i in range(0, len(list), size):
            yield list[i:i + size]

    def get_metrics_by_run_ids(self, run_ids):
        """Get multiple metrics by run history run ids.

        :param run_ids: Run Ids for the metrics to fetch. *Note* Best Metric value is retrieved
        and updated for these runs
        :type run_ids:
        :return: Transformed metric data in a friendly format.
        :rtype: dict
        """
        # Number of run ids per batch
        batch_size = 20

        if run_ids:
            # With hyperdrive/automl scenarios count of runs can get quite large and GET request limit may be reached
            # easily. We will need to group runs into batches and fetch the metrics based on defined degree
            # of parallelism.
            _batches = list(self.batches(sorted(run_ids), batch_size))
            trans_metrics = {}
            tasks = []

            for batch in _batches:
                result_as_generator = self.service_facade.get_metrics_by_run_ids(
                    run_ids=batch, custom_headers=self._common_headers,
                    orderby=['RunId asc'])
                tasks.append(result_as_generator)

            for task in tasks:
                # create friendly view of metrics; similar to what get_metrics returns for a single run
                for metric in task:
                    if metric.run_id not in trans_metrics:
                        trans_metrics[metric.run_id] = {}
                    run_metrics = trans_metrics[metric.run_id]
                    if metric.cells:
                        metric_name = metric.name
                        metric_type = metric.metric_type
                        for cell in metric.cells:
                            if metric_type == 'azureml.v1.scalar':
                                if metric_name in run_metrics:
                                    run_metrics[metric_name].append(cell[metric_name])
                                else:
                                    run_metrics[metric_name] = [cell[metric_name]]
                            elif metric_type == 'azureml.v1.table':
                                if metric_name not in run_metrics:
                                    run_metrics[metric_name] = {}
                                table_metrics = run_metrics[metric_name]
                                for metric_key, metric_value in cell.items():
                                    if metric_key in table_metrics:
                                        table_metrics[metric_key].append(metric_value)
                                    else:
                                        table_metrics[metric_key] = [metric_value]
            return trans_metrics
        return {}

    def _get_children(self, run_id, experiment, _rehydrate_runs=True, after_created_date=None, recursive=False):
        children = self.service_facade.get_child_runs(parent_run_id=run_id,
                                                      root_run_id=run_id,
                                                      recursive=recursive,
                                                      _filter_on_server=True, created=after_created_date)

        if _rehydrate_runs:
            return Run._rehydrate_runs(experiment, children)
        else:
            return (Run._dto_to_run(experiment, child) for child in children)
