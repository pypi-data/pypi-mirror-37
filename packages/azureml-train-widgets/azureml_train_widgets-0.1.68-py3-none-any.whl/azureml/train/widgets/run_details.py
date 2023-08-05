# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Common widget implementations shared between various platforms."""
import copy
import datetime
import json
import math
import operator
import re
import threading
import traceback
import time as systime
import urllib.request
import uuid
from dateutil import parser
from IPython.display import display
from multiprocessing.dummy import Pool
from urllib.error import HTTPError

from azureml.core.compute.batchai import BatchAiCompute
from azureml.train import _run_history_service_client
from azureml.train._telemetry_logger import _TelemetryLogger
from azureml._base_sdk_common import _ClientSessionId

from . import _platform
from ._constants import WIDGET_REFRESH_SLEEP_TIME, \
    WEB_WORKBENCH_PARENT_RUN_ENDPOINT, MULTIRUN_WIDGET_REFRESH_SLEEP_TIME
from ._transformer import _DataTransformer

# Jupyter Notebook
if _platform._in_jupyter_nb() is True:
    from . import _widgets
    PLATFORM = 'JUPYTER'
# Databricks and others
else:
    from . import _universal_widgets as _widgets
    PLATFORM = 'DATABRICKS'

logger = _TelemetryLogger.get_telemetry_logger(__name__)


class RunDetails:
    """
    Widget used for Training SDK run status

    :param run_instance: Run instance for which the widget will be rendered.
    :type run_instance: azureml.core.run.Run
    """

    def __new__(cls, run_instance):
        """Return corresponding run details widget based on run type.

        :param run_instance: Run instance for which the widget will be rendered.
        """
        _run_source_prop = 'azureml.runsource'
        widget_mapper = {
            'hyperdrive': _HyperDrive,
            'automl': _AutoML,
            'azureml.PipelineRun': _Pipeline,
            'azureml.StepRun': _StepRun,
            'experiment': _UserRun,
            'azureml.scriptrun': _UserRun
        }
        if run_instance.type is None:
            properties = run_instance.get_properties()
            if _run_source_prop in properties:
                run_type = properties[_run_source_prop].lower()
            else:
                run_type = 'experiment'
        else:
            run_type = run_instance.type

        return widget_mapper.get(run_type, _UserRun)(run_instance)

    def __init__(self, run_instance):
        """
        Initialize widget with provided run instance

        :param run_instance: Run instance for which the widget will be rendered.
        :type run_instance: azureml.core.run.Run
        """
        pass

    def show(self, render_lib=None, widget_settings=None):
        """
        Render widget and start thread to refresh the widget.

        :param render_lib: The library to use for rendering. Required only for databricks with value displayHTML
        :type render_lib: func
        :param widget_settings: Settings to be applied to widget. Supported settings are: 'debug' (boolean) and \
                                'display' (str, Supported values: 'popup': to show widget in a pop-up).
        :type widget_settings: dict
        """
        pass

    def get_widget_data(self, widget_settings=None):
        """
        Retrieve and transform data from run history to be rendered by widget. Used also for debugging purposes.

        :param widget_settings: Settings to be applied to widget. Supported settings are: 'debug' (boolean) and \
                                'display' (str, Supported values: 'popup': to show widget in a pop-up).
        :type widget_settings: dict
        :return: Dictionary containing data to be rendered by the widget.
        :rtype: dict
        """
        pass


class _WidgetBase(object):
    """Base class providing common methods by widgets."""

    def __init__(self, widget_sleep_time, widget):
        self.widget_instance = widget()
        self.widget_sleep_time = widget_sleep_time
        self.settings = {}
        self.isDebug = False
        self._pool = Pool()

    def __del__(self):
        """Destructor for the widget."""
        self._pool.close()

    def show(self, render_lib=None, widget_settings=None):
        """Render widget and start thread to refresh the widget.

        :param render_lib: The library to use for rendering.
        :type render_lib: func
        :param widget_settings: The widget settings.
        :type widget_settings: object
        """
        if widget_settings is None:
            widget_settings = {}

        widget_settings = {**self._get_default_setting(), **widget_settings}
        self.settings = widget_settings

        # pass the widget settings to client
        self.widget_instance.widget_settings = self.settings

        # if debug mode just return the data; do not render
        self.isDebug = 'debug' in self.settings and self.settings['debug']
        if self.isDebug:
            return self.get_widget_data(self.settings)

        # register events you want to subscribe to while taking actions on traitlets on client side
        try:
            self._register_events()
        except Exception as e:
            if self.isDebug:
                self.widget_instance.error = repr(traceback.format_exception(type(e), e, e.__traceback__))

        # render the widget
        telemetry_values = self._get_telemetry_values(self.show)
        with _TelemetryLogger.log_activity(logger,
                                           "train.widget.show",
                                           custom_dimensions=telemetry_values):
            try:
                display(self.widget_instance)
            except Exception as e:
                if render_lib is not None:
                    render_lib(self.widget_instance.get_html())
                if self.isDebug:
                    self.widget_instance.error = repr(traceback.format_exception(type(e), e, e.__traceback__))

        # refresh the widget in given interval
        thread = threading.Thread(target=self._refresh_widget, args=(render_lib, self.settings,))
        thread.start()
        if PLATFORM is 'DATABRICKS':
            thread.join()

    def _refresh_widget(self, render_lib, widget_settings):
        """Retrieve data from data source and update widget data value to reflect it on UI.

        :param render_lib: The library to use for rendering.
        :type render_lib: func
        :param widget_settings: The widget settings.
        :type widget_settings: object
        """
        telemetry_values = self._get_telemetry_values(self._refresh_widget)
        with _TelemetryLogger.log_activity(logger,
                                           "train.widget.refresh",
                                           custom_dimensions=telemetry_values) as activity_logger:
            lastError = None
            lastErrorCount = 0
            while True:
                try:
                    activity_logger.info(("Getting widget data..."))
                    widget_data = self.get_widget_data(widget_settings)
                    activity_logger.info(("Rendering the widget..."))
                    if render_lib is not None:
                        render_lib(self.widget_instance.get_html())
                    self.widget_instance.error = ''
                    if self._should_stop_refresh(widget_data):
                        activity_logger.info(("Stop auto refreshing..."))
                        self.widget_instance.is_finished = True
                        break
                    else:
                        systime.sleep(self.widget_sleep_time)
                        continue
                except Exception as e:
                    activity_logger.exception(e)

                    # only check exception type instead of value to avoid timestamp or some dynamic content
                    if type(e) == type(lastError):
                        lastErrorCount += 1
                    else:
                        lastError = e
                        lastErrorCount = 0

                    if lastErrorCount > 2:
                        if self.isDebug:
                            self.widget_instance.error = repr(traceback.format_exception(type(e), e, e.__traceback__))
                        else:
                            self.widget_instance.error = repr(traceback.format_exception_only(type(e), e))
                    continue

    def get_widget_data(self, widget_settings=None):
        """Abstract method for retrieving data to be rendered by widget."""
        pass

    def _should_stop_refresh(self, widget_data):
        pass

    def _register_events(self):
        pass

    def _register_event(self, callback, traitlet_name):
        self.widget_instance.observe(callback, names=traitlet_name)

    def _get_default_setting(self):
        return {"childWidgetDisplay": "popup"}

    def _get_telemetry_values(self, func):
        telemetry_values = {}

        # client common...
        telemetry_values['amlClientType'] = 'azureml-train-widget'
        telemetry_values['amlClientFunction'] = func.__name__
        telemetry_values['amlClientModule'] = self.__class__.__module__
        telemetry_values['amlClientClass'] = self.__class__.__name__
        telemetry_values['amlClientRequestId'] = str(uuid.uuid4())
        telemetry_values['amlClientSessionId'] = _ClientSessionId

        return telemetry_values


class _UserRun(_WidgetBase):
    """Generic run details widget."""

    _metrics_cache = {}
    _run_finished_states = ["completed", "failed", "canceled"]
    _str_waiting_log = "Your job is submitted in Azure cloud and we are monitoring to get logs..."
    _str_no_log = "Log is empty or no log files found."

    def __init__(self, run_instance, run_type="experiment", refresh_time=WIDGET_REFRESH_SLEEP_TIME,
                 widget=_widgets._UserRun, recursive_children=False, rehydrate_runs=False):
        self.experiment = run_instance.experiment
        self.run_instance = run_instance
        custom_headers = {'x-ms-synthetic-source': 'azureml-sdk-widget-' + run_type}
        self.run_history_service_client = _run_history_service_client._RunHistoryServiceClient(
            self.experiment,
            custom_headers=custom_headers)
        self.transformer = _DataTransformer.get_transformer(run_type)
        self.child_widget_instance = None
        self._transformed_child_runs_cache = []
        self._run_cache = {}
        self.run_properties = {}
        created_utc = self.run_instance._run_dto['created_utc']
        self.run_init_time = parser.parse(created_utc) if not isinstance(created_utc, datetime.datetime) \
            else created_utc
        self.run_type = run_type
        self.recursive_children = recursive_children
        self.rehydrate_runs = rehydrate_runs
        self.selected_process = None
        super().__init__(refresh_time, widget)

    @staticmethod
    def _sort_distributed_processes(distributed_processes):
        def ord_key_distributed_processes(process):
            # Direct alphanumeric comparison doesn't suffice- otherwise "worker_10" will show up before "worker_2"
            # Tuples compare in columnar order- SortBy(A, B, C) works like .Net's OrderBy(A).ThenBy(B).ThenBy(C)
            # Tupleize by underscores, casting columns to integers where possible to enforce numeric ordering.
            return tuple(int(s) if s.isdigit() else s for s in process.split("_"))
        return sorted(distributed_processes, key=ord_key_distributed_processes)

    def get_widget_data(self, widget_settings=None):
        """
        Retrieve and transform data from run history to be rendered by widget

        :param widget_settings: Settings to be applied to widget. Supported settings are: 'debug' and 'display'
        :type dict
        :return: Dictionary containing data to be rendered by the widget.
        :rtype: dict
        """
        if not self.settings:
            self.settings = widget_settings

        # set azure portal deep link for the run
        self.widget_instance.workbench_uri = self._get_web_workbench_run_detail_url(self.experiment)

        self.widget_instance.run_id = self.run_instance.id
        self.tags = self.run_instance.get_tags()

        run_properties_init = {'run_id': self.run_instance.id,
                               'created_utc': self.run_instance._run_dto['created_utc'],
                               'properties': self.run_instance.get_properties(),
                               'tags': self.tags}

        self.run_properties = {**self.run_properties, **run_properties_init}

        self.widget_instance.run_properties = self.run_properties

        self._pool.apply_async(func=self._get_run_metrics, callback=self._update_metrics)

        run_details = self.run_instance.get_details()

        self.error = run_details.get("error")
        run_config = run_details.get("runDefinition")
        requested_node_count = 0

        if run_config:
            self.run_properties['script_name'] = run_config['Script'] if 'Script' in run_config else None
            self.run_properties['arguments'] = " ".join(run_config['Arguments']) \
                if 'Arguments' in run_config and run_config['Arguments'] else None
            batch_ai = run_config.get('BatchAi')
            if batch_ai:
                requested_node_count = batch_ai.get('NodeCount')

        self._pool.apply_async(func=self._get_compute_target_status, args=(run_details.get("target"),
                                                                           requested_node_count),
                               callback=self._update_compute_target_status)

        # get parent run properties
        self.run_properties['end_time_utc'] = run_details.get("endTimeUtc")
        self.run_properties['status'] = run_details.get("status")
        self.run_properties['log_files'] = run_details.get("logFiles")

        # log file names have process names embedded within the name which we need to extract
        distributed_processes = []
        log_files = run_details.get("logFiles")
        if log_files:
            for file in log_files.keys():
                found_group = re.search(r'log_(.*[0-9]*).txt$', file)
                if found_group is not None:
                    process_name = found_group.group(1)
                    if process_name not in distributed_processes:
                        distributed_processes.append(process_name)

        self.run_properties['distributed_processes'] = _UserRun._sort_distributed_processes(distributed_processes)

        self._add_additional_properties(self.run_properties)

        run_properties_temp = copy.deepcopy(self.run_properties)
        run_properties_temp['SendToClient'] = '1'
        self.widget_instance.run_properties = run_properties_temp
        self.properties = self.run_properties['properties']

        if self.selected_process:
            _run_process = self.selected_process
        else:
            _run_process = self.run_properties['distributed_processes'][0] \
                if self.run_properties['distributed_processes'] else None
        self._get_run_logs_async(log_files,
                                 run_details.get("status"),
                                 self.error,
                                 _run_process)

        child_runs = self._get_child_runs()

        # Widget renders child runs in two phases. In phase one it retrieves the child runs from backend and
        # renders them with corresponding properties. Then, in second phase, when their metrics are retrieved
        # it renders child runs again, this time it updates each child run with its corresponding best metric value.
        # we keep this cache for two purposes:
        # 1. so that in next refresh iteration we do not lose the metrics and user keeps seeing
        # updated child runs on the client
        # 2. Only query the backend for runs that are not completed
        copy_cache = copy.deepcopy(self._transformed_child_runs_cache)
        for c in child_runs:
            _run = next((x for x in copy_cache if x['run_number'] == c['run_number']), None)
            if not _run:
                # todo: switch to dict
                copy_cache.append(c)
            else:
                ind = copy_cache.index(_run)
                copy_cache[ind] = {**_run, **c}

        self.widget_instance.child_runs = copy_cache
        self._transformed_child_runs_cache = copy_cache

        # get the run with smallest datetime that is already running. We do not need to get the older runs as they
        # are completed and cached
        incomplete_runs = [x for x in self._transformed_child_runs_cache if x['status'].lower() not in
                           _UserRun._run_finished_states]
        if incomplete_runs:
            self.run_init_time = min(x['created_time_dt'] for x in incomplete_runs)

        transformed_children_metrics = {}
        if self._transformed_child_runs_cache:
            run_ids = [x['run_id'] for x in self._transformed_child_runs_cache]

            metrics = {}

            # get list of not cached runs for which we will retrieve metrics
            not_cached_runs = [x for x in self._transformed_child_runs_cache if x['run_id']
                               not in _UserRun._metrics_cache]
            if not_cached_runs:
                metrics = self._get_metrics(not_cached_runs)

                # populate cache with metrics from completed runs
                completed_run_ids = [x['run_id'] for x in self._transformed_child_runs_cache
                                     if x['status'].lower() in _UserRun._run_finished_states]
                metrics_to_be_cached = {k: v for k, v in metrics.items() if k in completed_run_ids}
                _UserRun._metrics_cache = {**_UserRun._metrics_cache, **metrics_to_be_cached}

            cached_run_metrics = {k: v for k, v in _UserRun._metrics_cache.items() if k in run_ids}
            metrics = {**cached_run_metrics, **metrics}

            mapped_metrics = self._get_mapped_metrics(metrics, self._transformed_child_runs_cache)

            transformed_children_metrics = self.transformer.transform_widget_metric_data(mapped_metrics,
                                                                                         self._get_primary_config())
            self.widget_instance.child_runs_metrics = transformed_children_metrics

            updated_runs = self._update_children_with_metrics(self._transformed_child_runs_cache,
                                                              transformed_children_metrics)
            if updated_runs:
                self._transformed_child_runs_cache = sorted(updated_runs, key=operator.itemgetter("run_number"))
                self.widget_instance.child_runs = self._transformed_child_runs_cache

        return {'status': self.run_properties['status'],
                'workbench_run_details_uri': self._get_web_workbench_run_detail_url(self.experiment),
                'run_id': self.run_instance.id,
                'run_properties': self.run_properties,
                'child_runs': self.widget_instance.child_runs,
                'children_metrics': self.widget_instance.child_runs_metrics,
                'run_metrics': self.widget_instance.run_metrics,
                'run_logs': self.widget_instance.run_logs,
                'widget_settings': widget_settings}

    def _add_additional_properties(self, run_properties):
        run_properties['run_duration'] = self.transformer._get_run_duration(run_properties['status'],
                                                                            run_properties['created_utc'],
                                                                            run_properties['end_time_utc'])

    def _get_compute_target_status(self, target_name, requested_node_count):
        ws_targets = []
        try:
            ws_targets = self.experiment.workspace.compute_targets()
        except Exception as e:
            if self.isDebug:
                logger.warning(e)

        for ct_name in ws_targets:
            ct = ws_targets[ct_name]
            if ct.name == target_name and type(ct) is BatchAiCompute:
                ct_dict = {
                    "provisioning_state": ct.provisioning_state,
                    "provisioning_errors": ct.provisioning_errors
                }
                status_dict = {}
                ct_status = ct.get_status()
                if ct_status:
                    status_dict = {
                        "node_state_counts": ct_status.node_state_counts.serialize(),
                        "scale_settings": ct_status.scale_settings.serialize(),
                        "vm_size": ct_status.vm_size,
                        "current_node_count": ct_status.current_node_count,
                        "requested_node_count": requested_node_count
                    }
                return {**ct_dict, **status_dict}
        return {}

    def _update_compute_target_status(self, result):
        self.widget_instance.compute_target_status = result

    def _get_run_logs_async(self, log_files, status, error, process):
        self._pool.apply_async(func=self._get_run_logs, args=(log_files, status, error, process),
                               callback=self._update_logs)

    def _get_run_logs(self, log_files, status, error, process):
        _status = status.lower()
        logs = _UserRun._str_no_log \
            if _status in _UserRun._run_finished_states \
            else _UserRun._str_waiting_log
        _logs = ''

        if log_files:
            _logs = self._get_formatted_logs(log_files, process)

        if error:
            inner_error = error.get('error')
            error_message = inner_error.get('message') if inner_error else ""
            _error = "" if not error_message else "{0}\n".format(error_message)
            _logs = "{0}\nError occurred: {1}".format(_logs, _error)
        elif _status in ['completed', 'canceled']:
            _logs = "{0}\nRun is {1}.".format(_logs, _status)

        if _logs:
            logs = _logs
        return logs

    def _get_formatted_logs(self, log_files, process):
        _process = "_{0}".format(process) if process else ""
        return "{0}{1}{2}{3}".format(self._get_log('ice_log', log_files),
                                     self._get_log('image_build_log', log_files),
                                     self._get_log('control_log' + _process, log_files),
                                     self._get_log('driver_log' + _process, log_files))

    def _get_log(self, log_type, log_files):
        log_uri = [v for (k, v) in log_files.items() if log_type in k]
        if log_uri:
            url = log_uri[0]
            try:
                response = urllib.request.urlopen(url)
                log_content_bytes = response.read()
                log_content = self._post_process_log(log_content_bytes.decode('utf-8'))
                return "{}\n".format(log_content)
            except HTTPError as e:
                if self.isDebug:
                    self.widget_instance.error = repr(traceback.format_exception(type(e), e, e.__traceback__))
                return ''
        return ''

    def _post_process_log(self, log_content):
        return log_content

    def _update_logs(self, result):
        self.widget_instance.run_logs = result

    def _get_child_runs(self):
        # put a buffer for look-back due to time sync
        buffered_init_time = self.run_init_time - datetime.timedelta(seconds=20)
        child_runs = self.run_history_service_client._get_children(run_id=self.run_instance.id,
                                                                   experiment=self.experiment,
                                                                   after_created_date=buffered_init_time,
                                                                   recursive=self.recursive_children,
                                                                   _rehydrate_runs=self.rehydrate_runs)

        child_runs_list = list(child_runs)
        for run in child_runs_list:
            self._run_cache[run.id] = run

        return self.transformer.transform_widget_run_data(child_runs_list)

    def _get_run_metrics(self):
        run_metrics = self.run_instance.get_metrics()
        transformed_run_metrics = []

        for key, value in run_metrics.items():
            metric_data = {
                'name': key,
                'run_id': self.run_instance.id,
                # get_metrics can return array or not based on metrics being series or scalar value
                'categories': list(range(len(value))) if isinstance(value, list) else [0],
                'series': [{'data': value if isinstance(value, list) else [value]}]}
            transformed_run_metrics.append(metric_data)
        return transformed_run_metrics

    def _update_metrics(self, result):
        self.widget_instance.run_metrics = result

    def _get_metrics(self, child_runs):
        return self.run_history_service_client.get_metrics_by_run_ids([run['run_id'] for run in child_runs])

    def _get_mapped_metrics(self, metrics, child_runs):
        run_number_mapper = {c['run_id']: c['run_number'] for c in child_runs}
        return {run_number_mapper[k]: v for k, v in metrics.items()}

    def _update_children_with_metrics(self, child_runs, metrics):
        pass

    def _get_web_workbench_run_detail_url(self, experiment):
        """Generate the web workbench job url for the run details.

        :param experiment: The experiment.
        :type experiment: azureml.core.experiment.Experiment
        """
        # TODO: Host to web workbench needs to be retrieved
        return (WEB_WORKBENCH_PARENT_RUN_ENDPOINT).format(
            experiment.workspace.subscription_id,
            experiment.workspace.resource_group,
            experiment.workspace.name,
            experiment.name,
            self.run_instance.id)

    def _get_primary_config(self):
        if self.settings and 'Metric' in self.settings:
            return {
                'name': self.settings['Metric']['name'],
                'goal': self.settings['Metric']['goal'] if 'goal' in self.settings['Metric'] else 'minimize'
            }
        return {}

    def _should_stop_refresh(self, widget_data):
        return widget_data['run_properties']['status'] is not None and \
            widget_data['run_properties']['status'].lower() in _UserRun._run_finished_states

    def _register_events(self):
        self._register_event(self._on_selected_run_id_change, "selected_run_id")
        self._register_event(self._on_run_process_change, "run_process")

    def _on_run_process_change(self, change):
        self.selected_process = change.new
        self._get_run_logs_async(self.widget_instance.run_properties['log_files'],
                                 self.widget_instance.run_properties['status'],
                                 self.error, change.new)

    def _on_selected_run_id_change(self, change):
        # work around about close of popup, selected_run_id is set to empty string right after with it is set
        # with value
        if change.new == '':
            return
        if self.child_widget_instance is not None and change.new != '':
            self.child_widget_instance.close()
        if self.widget_instance.child_runs:
            run_list = [x for x in self.widget_instance.child_runs if x['run_id'] == change.new]
            if len(run_list) > 0:
                run = self._run_cache[change.new]
                selected_run_widget = RunDetails(run)
                display_setting = self.settings["childWidgetDisplay"] if "childWidgetDisplay" in self.settings else ""
                selected_run_widget.show(widget_settings={'display': display_setting})
                self.child_widget_instance = selected_run_widget.widget_instance

    def _get_telemetry_values(self, func):
        telemetry_values = super()._get_telemetry_values(func)
        telemetry_values['widgetRunType'] = self.run_type
        return telemetry_values


class _HyperDrive(_UserRun):
    """Hyperdrive run details widget."""

    def __init__(self, run_instance):
        """Initialize a HyperDrive widget call.

        :param run_instance: The hyperdrive run instance.
        :type run_instance: HyperDriveRun
        """
        super().__init__(run_instance, "HyperDrive", refresh_time=MULTIRUN_WIDGET_REFRESH_SLEEP_TIME,
                         widget=_widgets._HyperDrive)

    def _update_children_with_metrics(self, child_runs, metrics):
        # for each child run add their corresponding best metric reached so far
        if metrics and metrics['series']:
            child_runs_local = copy.deepcopy(child_runs)

            pmc_goal = self._get_primary_config()['goal']
            pmc_name = self._get_primary_config()['name']
            func = max if pmc_goal == 'maximize' else min

            # check chart type. if there is 'run_id' in series that means each series corresponds to a run id
            # which corresponds to hyperdrive chart with line series, else it's scattered chart
            if metrics['series'][pmc_name] and 'run_id' in metrics['series'][pmc_name][0]:
                for series in metrics['series'][pmc_name]:
                    run = next(x for x in child_runs_local if x['run_number'] == series['run_id'])
                    if run:
                        run['best_metric'] = func(series['data'])
            else:
                goal_name = '_min' if pmc_goal == 'minimize' else '_max'
                primary_metric = {}
                best_metric = {}

                for _key, dataList in metrics['series'].items():
                    for x in dataList:
                        if x['name'] == pmc_name:
                            primary_metric = dict(zip(x['categories'], x['data']))
                        elif x['name'] == pmc_name + goal_name:
                            best_metric = dict(zip(x['categories'], x['data']))

                for num in range(0, len(child_runs_local)):
                    run_number = child_runs_local[num]['run_number']
                    child_runs_local[num]['metric'] = round(primary_metric[run_number], 8) \
                        if run_number in primary_metric \
                        and not math.isnan(float(primary_metric[run_number])) else None
                    child_runs_local[num]['best_metric'] = round(best_metric[run_number], 8) \
                        if run_number in best_metric \
                        and not math.isnan(float(best_metric[run_number])) else None

            return child_runs_local

    def _add_additional_properties(self, run_properties):
        super()._add_additional_properties(run_properties)

        tags = run_properties['tags']
        if 'generator_config' in tags:
            generator_config = json.loads(tags['generator_config'])
            run_properties['hyper_parameters'] = generator_config['parameter_space']

    def _get_child_runs(self):
        _child_runs = super()._get_child_runs()

        for run in _child_runs:
            run_id = run['run_id']
            if run_id in self.tags:
                arguments = json.loads(self.tags[run_id])
                if arguments:
                    for name, value in arguments.items():
                        run['param_' + name] = value

        return _child_runs

    def _post_process_log(self, log_content):
        # Hyperdrive currently has additional start and end tags with no line-break (due to a bug in artifact service
        # Below logic splits log content into lines based on these tags
        lines = re.findall(r'(?<=<START>)(.*?)(?=<END>)', log_content)
        if lines:
            return '\r\n'.join(lines)
        return log_content

    def _get_formatted_logs(self, log_files, rank):
        return self._get_log('hyperdrive', log_files)

    def _get_primary_config(self):
        collection = self.properties if 'primary_metric_config' in self.properties else self.tags
        c = json.loads(collection['primary_metric_config'])
        config = {
            'name': c['name'],
            'goal': c['goal']
        }
        return config


class _AutoML(_UserRun):
    """AutoML run details widget."""

    def __init__(self, run_instance):
        """Initialize a Run Details widget call.

        :param run_instance: automl run instance.
        :type run_instance: AutoMLRun
        """
        super().__init__(run_instance, "automl", refresh_time=30,
                         widget=_widgets._AutoML)

    def _update_children_with_metrics(self, child_runs, metrics):
        # for each child run add their corresponding primary metric values amd best metric reached so far
        if metrics and metrics['series']:
            child_runs_local = copy.deepcopy(child_runs)

            pmc = self._get_primary_config()['name']
            pmc_goal = self._get_primary_config()['goal']
            goal_name = '_min' if pmc_goal == 'minimize' else '_max'
            primary_metric = {}
            best_metric = {}

            for _key, dataList in metrics['series'].items():
                for x in dataList:
                    if x['name'] == pmc:
                        primary_metric = dict(zip(x['categories'], x['data']))
                    elif x['name'] == pmc + goal_name:
                        best_metric = dict(zip(x['categories'], x['data']))

            for num in range(0, len(child_runs_local)):
                iteration = child_runs_local[num]['iteration']
                if iteration in primary_metric:
                    child_runs_local[num]['primary_metric'] = round(primary_metric[iteration], 8) \
                        if iteration in primary_metric \
                        and not math.isnan(float(primary_metric[iteration])) else None
                    child_runs_local[num]['best_metric'] = round(best_metric[iteration], 8) \
                        if iteration in best_metric \
                        and not math.isnan(float(best_metric[iteration])) else None

            return child_runs_local

    def _get_mapped_metrics(self, metrics, child_runs):
        run_number_mapper = {c['run_id']: c['iteration'] for c in child_runs}
        return {run_number_mapper[k]: v for k, v in metrics.items()}

    def _get_metrics(self, child_runs):
        metrics = super()._get_metrics(child_runs)

        pmc = self._get_primary_config()['name']
        goal_name = '_min' if self._get_primary_config()['goal'] == 'minimize' else '_max'

        # Automl currently populates the max field; remove that to resolve conflict
        for run_id in metrics:
            metrics[run_id].pop(pmc + goal_name, None)

        return metrics

    def _get_primary_config(self):
        config_settings = json.loads(self.properties['AMLSettingsJsonString'])
        config = {
            'name': config_settings['primary_metric'],
            'goal': config_settings['metric_operation']
        }
        return config


class _StepRun(_UserRun):
    """StepRun run details widget."""

    def __init__(self, run_instance):
        """Initialize a StepRun widget call.

        """
        super().__init__(run_instance, "Pipeline", refresh_time=MULTIRUN_WIDGET_REFRESH_SLEEP_TIME,
                         widget=_widgets._UserRun, rehydrate_runs=True)

    def _get_run_logs_async(self, log_files, status, error, process):
        self._pool.apply_async(func=self._get_run_logs, args=(log_files, status, error, process),
                               callback=self._update_logs)

    def _get_run_logs(self, log_files, status, error, process):
        _status = status.lower()
        logs = _UserRun._str_waiting_log \
            if _status in _UserRun._run_finished_states \
            else _UserRun._str_no_log

        stdout_log = self.run_instance.get_stdout_log()
        stderr_log = self.run_instance.get_stderr_log()
        job_log = self.run_instance.get_job_log()
        if stdout_log or stderr_log or job_log:
            return "{0}\n{1}\nError occurred: {2}\n.".format(job_log, stdout_log, stderr_log)
        else:
            return logs


class _Pipeline(_UserRun):
    """Pipeline run details widget."""

    def __init__(self, run_instance):
        """Initialize a Pipeline widget call.

        """
        super().__init__(run_instance, "Pipeline", refresh_time=MULTIRUN_WIDGET_REFRESH_SLEEP_TIME,
                         widget=_widgets._Pipeline, rehydrate_runs=True)

    def get_widget_data(self, widget_settings=None):
        widget_data = super().get_widget_data(widget_settings)
        graph = self.transformer._transform_graph(self.run_instance.get_graph(),
                                                  list(self._run_cache.values()))
        widget_data['child_runs'] = graph['child_runs']
        widget_data['graph'] = graph
        self.widget_instance.child_runs = graph['child_runs']
        self.widget_instance.graph = graph
        return widget_data
