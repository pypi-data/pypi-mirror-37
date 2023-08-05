# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Service to client JS transformer."""

import math
import re
from datetime import datetime, timedelta, timezone
from dateutil import parser
from azureml.pipeline.core import StepRun


class _DataTransformer(object):
    """Base class for run object transformer."""

    MINIMIZE = 'minimize'

    def transform_widget_metric_data(self, metrics, primary_metric_config):
        """Transform run's metric data to JS consumable format.

        :param metrics: list of all metrics for a hyperdrive experiment
        :param primary_metric_config: primary metric config for the hyperdrive experiment
        :return: transformed metrics list in form [{'categories': [...], 'series': [{...}, {...}], 'metricName':
                'metricname', 'primaryGoalValues': {...}}, {...}]
        """
        transformed_metrics = {
            'categories': None,
            'series': None,
            'metricName': None}

        # Validate input metric list
        if metrics is None or len(metrics) < 1:
            return transformed_metrics

        # Root dictionary for all metric series
        all_series = {}

        # Transform metric data in widget consumable format
        for run_number, run_metrics in metrics.items():
            series_name = run_number
            for metric_name, series_data in run_metrics.items():
                metric_data = {
                    'run_id': run_number,
                    'name': series_name,
                    'data': series_data,
                    'mode': 'lines',
                    'stepped': False}
                if metric_name in all_series:
                    all_series[metric_name].append(metric_data)
                else:
                    all_series[metric_name] = [metric_data]

        pmc_name = primary_metric_config['name']
        pmc_goal = primary_metric_config['goal']

        transformed_metrics['series'] = all_series
        # categories in x-axis will be the range from 1 to max of cell counts of all runs
        transformed_metrics['categories'] = list(range(max(len(x['data']) for x in all_series[pmc_name])))
        transformed_metrics['primaryMetricName'] = pmc_name
        transformed_metrics['showLegend'] = True

        # check whether any metrics have more than one value reported per run
        # if not then we'll need to use scattered chart and metrics need to be re-transformed accordingly
        a = next((x for x in all_series[pmc_name] if len(x['data']) > 1), None)
        if a is None:
            self._retransform_metrics(transformed_metrics, pmc_name, pmc_goal)

        return transformed_metrics

    @staticmethod
    def _get_target_series_by_goal(func, series):
        # apply the goal function for each item in the series
        # we already know at this point that there is one item in 'data' array
        pmc_goal_data = [series[0]['data'][0]]
        cur_goal = pmc_goal_data[0]

        for i in range(1, len(series)):
            cur_value = series[i]['data'][0]
            if not math.isnan(float(cur_value)):
                cur_goal = cur_value if math.isnan(float(cur_goal)) else func(cur_goal, cur_value)
            pmc_goal_data.append(cur_goal)

        return pmc_goal_data

    def _retransform_metrics(self, metrics, pmc_name, pmc_goal):
        """
        Secondary transform of metrics in case each run's metrics are scalar values.

        With this transform x-axis becomes run number and y-axis metric value.
        """
        if metrics['series']:
            newSeries = {}
            for name, series in metrics['series'].items():
                # sorted job ids will be the x-axis
                series.sort(key=lambda x: int(x['name']))
                # skip the metrics of table type as it's not needed in primary metric chart
                if not type(series[0]['data']) is dict:
                    if isinstance(series[0]['data'][0], float) or isinstance(series[0]['data'][0], int):
                        mc_goal_data = self._get_target_series_by_goal(min if pmc_goal == self.MINIMIZE else max,
                                                                       series)
                    else:
                        mc_goal_data = []
                    list_mc = {
                        'categories': [child['name'] for child in series],
                        'mode': 'markers',
                        'name': name,
                        'stepped': False,
                        'type': 'scatter',
                        'data': [child['data'][0] if len(child['data']) > 0 else 0 for child in series]}

                    list_mc_goal = {
                        'categories': [child['name'] for child in series],
                        'mode': 'lines',
                        'name': "{}_{}".format(name, 'min' if pmc_goal == self.MINIMIZE else 'max'),
                        'stepped': True,
                        'type': 'scatter',
                        'data': mc_goal_data}
                    newSeries[name] = [list_mc, list_mc_goal]

            metrics['series'] = newSeries
            metrics['showLegend'] = False

        return metrics

    @staticmethod
    def get_transformer(run_type):
        """Return transformer instance based on run's type."""
        return {
            'hyperdrive': _HyperDriveDataTransformer(),
            'automl': _AutoMLDataTransformer(),
            'pipeline': _PipelineGraphTransformer(),
        }.get(run_type.lower(), _DataTransformer())

    @staticmethod
    def _get_run_duration(status, created_utc, end_time_utc=None):
        if status.lower() == 'notresponding':
            return None
        if end_time_utc is None:
            end_time = datetime.now(timezone.utc)
        else:
            end_time = end_time_utc
            if not isinstance(end_time_utc, datetime):
                end_time = parser.parse(end_time_utc)

        # in duration calculation include queue time. use created time instead of started time.
        created_time = created_utc
        if not isinstance(created_time, datetime):
            created_time = parser.parse(created_time)

        if created_time in (None, ''):
            duration_secs = 0
        else:
            duration_secs = max((end_time - created_time).total_seconds(), 0)

        delta = timedelta(seconds=duration_secs)
        # truncate microseconds
        return str(delta - timedelta(microseconds=delta.microseconds))

    def _transform_run(self, run):
        top_level_properties = run._run_dto
        return dict(run_id=run.id, run_number=top_level_properties['run_number'], metric=None,
                    status=top_level_properties['status'],
                    start_time=top_level_properties['start_time_utc'].__str__()
                    if 'start_time_utc' in top_level_properties else '',
                    end_time=top_level_properties['end_time_utc'].__str__()
                    if 'end_time_utc' in top_level_properties else '',
                    created_time=top_level_properties['created_utc'].__str__()
                    if 'created_utc' in top_level_properties else '',
                    created_time_dt=top_level_properties['created_utc']
                    if 'created_utc' in top_level_properties else '',
                    duration=_DataTransformer._get_run_duration(top_level_properties['status'],
                                                                top_level_properties['created_utc']
                                                                if 'created_utc' in top_level_properties else None,
                                                                top_level_properties['end_time_utc']
                                                                if 'end_time_utc' in top_level_properties else None))

    def transform_widget_run_data(self, runs):
        """Transform needed run properties."""
        transformed_jobs = []
        for run in runs:
            transformed_run = self._transform_run(run)
            transformed_run = {**transformed_run, **self._get_additional_properties(run)}
            transformed_jobs.append(transformed_run)
        return transformed_jobs

    def _get_additional_properties(self, run):
        return {}


class _AutoMLDataTransformer(_DataTransformer):
    """Transform run and metric data for AutoML runs."""

    def _get_additional_properties(self, run):
        property_bag = run._run_dto['properties']
        top_level_properties = run._run_dto
        goal = property_bag['goal'] if 'goal' in property_bag else None
        run_properties = property_bag['run_properties'] if 'run_properties' in property_bag else None

        if 'run_preprocessor' in property_bag and 'run_algorithm' in property_bag:
            if property_bag['run_preprocessor']:
                run_name = "{0}, {1}".format(property_bag['run_preprocessor'], property_bag['run_algorithm'])
            else:
                run_name = property_bag['run_algorithm']
        else:
            run_name = top_level_properties['status']
        return {
            'iteration': property_bag['iteration'],
            'goal': goal,
            'run_name': run_name,
            'run_properties': run_properties
        }


class _HyperDriveDataTransformer(_DataTransformer):
    """Transform run and metric data for HyperDrive runs."""

    def _get_additional_properties(self, run):
        property_bag = run._run_dto['properties']
        arguments = property_bag['Arguments'] if 'Arguments' in property_bag else None
        hyperdrive_job_id = self._get_hyperdrive_run_id(run.id)

        return {
            'hyperdrive_id': hyperdrive_job_id,
            'arguments': arguments
        }

    @staticmethod
    def _get_hyperdrive_run_id(run_id):
        found_group = re.search(r'([^_]*)_[^_]*$', run_id)
        if found_group is not None:
            return found_group.group(1)
        return run_id


class _PipelineGraphTransformer(_DataTransformer):

    def _transform_graph(self, graph, child_runs):
        transform_graph = {
            'datasource_nodes': {},
            'module_nodes': {},
            'edges': [],
            'child_runs': {}
        }

        if graph:
            for node in graph.datasource_nodes:
                transform_graph['datasource_nodes'][node.node_id] = {
                    'node_id': node.node_id,
                    'name': node.name
                }

            for node in graph.module_nodes:
                transform_graph['module_nodes'][node.node_id] = {
                    'node_id': node.node_id,
                    'name': node.name,
                    'status': 'NotStarted',
                }
                transform_graph['child_runs'][node.node_id] = {
                    'run_number': '',
                    'run_id': '',
                    'name': node.name,
                    'status': 'NotStarted',
                    'start_time': '',
                    'created_time': '',
                    'end_time': '',
                    'duration': ''
                }

            for node in graph.module_nodes:
                for node_input in node.inputs:
                    if node_input.incoming_edge is not None:
                        source_node = node_input.incoming_edge.source_port.node
                        transform_graph['edges'].append({
                            'source_node_id': source_node.node_id,
                            'source_node_name': source_node.name,
                            'name': ''.join(list(source_node.output_dict.keys())[0]),
                            'dst_node_id': node.node_id,
                            'dst_node_name': node.name
                        })

            for child_run in child_runs:
                if not isinstance(child_run, StepRun):
                    continue

                if child_run._is_reused:
                    node_id = child_run._current_node_id
                else:
                    node_id = child_run._node_id
                transform_graph['module_nodes'][node_id]['_is_reused'] = child_run._is_reused

                node = graph.get_node(node_id)

                transform_graph['module_nodes'][node_id]['number'] = child_run.number
                transform_graph['module_nodes'][node_id]['status'] = child_run.get_status()
                transform_graph['module_nodes'][node_id]['run_id'] = child_run.id
                transform_run = self._transform_run(child_run)
                transform_run['name'] = node.name
                transform_run['is_reused'] = "Yes" if child_run._is_reused else ""
                transform_graph['child_runs'][node_id] = {**transform_graph['child_runs'][node_id], **transform_run}
                transform_graph['child_runs'][node_id]['status'] = child_run.get_status()

            transform_graph['child_runs'] = list(transform_graph['child_runs'].values())
        return transform_graph
