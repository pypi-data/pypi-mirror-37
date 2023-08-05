# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# ---------------------------------------------------------

"""Access RunHistoryClient"""
import six

from .contracts.events import (create_heartbeat_event, create_start_event,
                               create_failed_event, create_completed_event,
                               create_canceled_event)
from .contracts.utils import get_run_ids_filter_expression, get_new_id
from .models.create_run_dto import CreateRunDto
from .experiment_client import ExperimentClient
from .constants import (RUN_ID_EXPRESSION, ORDER_BY_STARTTIME_EXPRESSION,
                        ORDER_BY_RUNID_EXPRESSION)
from ._odata.expressions import and_join
from ._odata.runs import get_filter_run_tags, get_filter_run_properties, get_filter_run_type, \
    get_filter_run_created_after
from ._hierarchy.runs import Tree


DEFAULT_PAGE_SIZE = 50


class RunHistoryClient(ExperimentClient):
    """
    Run History APIs

    :param host: The base path for the server to call.
    :type host: str
    :param auth: Authentication for the client
    :type auth: azureml.core.authentication.AbstractAuthentication
    :param subscription_id:
    :type subscription_id: str
    :param resource_group_name:
    :type resource_group_name: str
    :param workspace_name:
    :type workspace_name: str
    :param experiment_name:
    :type experiment_name: str
    """

    @staticmethod
    def create(workspace, experiment_name, _host=None, **kwargs):
        """
        Create a RunHistoryClient for the history
        :param workspace: User's workspace
        :type workspace: azureml.core.workspace.Workspace
        :param experiment_name:
        :type experiment_name: str
        """
        return RunHistoryClient(_host, workspace._auth_object, workspace.subscription_id,
                                workspace.resource_group, workspace.name, experiment_name,
                                **kwargs)

    def get_events(self, run_id):
        """
        Get events of a run by its run_id
        :param str run_id:  (required)
        :return: a generator of ~_restclient.models.BaseEvent
        """
        order_expression = [ORDER_BY_STARTTIME_EXPRESSION]
        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_project_arguments(self._client.legacy_events.list,
                                                        run_id=run_id,
                                                        orderby=order_expression,
                                                        is_paginated=True)

        return self._execute_with_project_arguments(self._client.events.list,
                                                    run_id=run_id,
                                                    orderby=order_expression,
                                                    is_paginated=True)

    def post_event(self, run_id, event, is_async=False):
        """
        Post an event of a run by its run_id
        This method makes a synchronous call by default. To make an
        asynchronous call, please pass is_async=True
        :param str run_id:  (required)
        :param models.BaseEvent object (required)
        :param is_async bool: execute request asynchronously
        :return:
            If is_async parameter is True,
            the request is called asynchronously.
            The method returns azureml._async.AsyncTask object
            If parameter is_async is False or missing,
            the method returns None.
        """
        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_project_arguments(self._client.legacy_events.post,
                                                        run_id=run_id,
                                                        event_message=event,
                                                        is_async=is_async)

        return self._execute_with_project_arguments(self._client.events.post,
                                                    run_id=run_id,
                                                    event_message=event,
                                                    is_async=is_async)

    def post_event_run_start(self, run_id, is_async=False):
        """
        Post run-started-event by its run_id
        This method makes a synchronous call by default. To make an
        asynchronous call, please pass is_async=True
        :param str run_id:  (required)
        :param is_async bool: execute request asynchronously
        :return:
            If is_async parameter is True,
            the request is called asynchronously.
            The method returns azureml._async_task.AsyncTask object
            If parameter is_async is False or missing,
            the method returns None.
        """
        event = create_start_event(run_id)
        return self.post_event(run_id, event, is_async)

    def post_event_run_failed(self, run_id, is_async=False):
        """
        Post run-failed-event by its run_id
        This method makes a synchronous call by default. To make an
        asynchronous call, please pass is_async=True
        :param str run_id:  (required)
        :param is_async bool: execute request asynchronously
        :return:
            If is_async parameter is True,
            the request is called asynchronously.
            The method returns azureml._async.AsyncTask object
            If parameter is_async is False or missing,
            the method returns None.
        """
        event = create_failed_event(run_id)
        return self.post_event(run_id, event, is_async)

    def post_event_run_completed(self, run_id, is_async=False):
        """
        Post run-completed-event by its run_id
        This method makes a synchronous call by default. To make an
        asynchronous call, please pass is_async=True
        :param str run_id:  (required)
        :param is_async bool: execute request asynchronously
        :return:
            If is_async parameter is True,
            the request is called asynchronously.
            The method returns azureml._async.AsyncTask object
            If parameter is_async is False or missing,
            the method returns None.
        """
        event = create_completed_event(run_id)
        return self.post_event(run_id, event, is_async)

    def post_event_run_canceled(self, run_id, is_async=False):
        """
        Post run-canceled-event by its run_id
        This method makes a synchronous call by default. To make an
        asynchronous call, please pass is_async=True
        :param str run_id:  (required)
        :param is_async bool: execute request asynchronously
        :return:
            If is_async parameter is True,
            the request is called asynchronously.
            The method returns azureml._async.AsyncTask object
            If parameter is_async is False or missing,
            the method returns None.
        """
        event = create_canceled_event(run_id)
        return self.post_event(run_id, event, is_async)

    def post_event_run_heartbeat(self, run_id, time, is_async=False):
        """
        Post run-heartbeat-event by its run_id
        This method makes a synchronous call by default. To make an
        asynchronous call, please pass is_async=True
        :param str run_id:  (required)
        :param int time: timeout in seconds (required)
        :param is_async bool: execute request asynchronously
        :return:
            If is_async parameter is True,
            the request is called asynchronously.
            The method returns azureml._async.AsyncTask object
            If parameter is_async is False or missing,
            the method returns None.
        """
        event = create_heartbeat_event(run_id, time)
        return self.post_event(run_id, event, is_async)

    def create_run(self, run_id=None, script_name=None, target=None,
                   run_name=None, create_run_dto=None, is_async=False):
        """
        create a run
        This method makes a synchronous call by default. To make an
        asynchronous call, please pass is_async=True
        :param str run_id: run id
        :param str script_name: script name
        :param str target: run target
        :param str run_name: run name
        :param CreateRunDto create_run_dto: run object to create
        :param is_async bool: execute request asynchronously
        :return:
            If is_async parameter is True,
            the request is called asynchronously.
            The method returns azureml._async.AsyncTask object
            If parameter is_async is False or missing,
            the method returns ~_restclient.models.RunDto.
        """
        run_id = get_new_id() if run_id is None else run_id
        if not create_run_dto or not isinstance(create_run_dto, CreateRunDto):
            create_run_dto = CreateRunDto(run_id=run_id,
                                          script_name=script_name,
                                          target=target,
                                          name=run_name,
                                          status='NotStarted')

        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_project_arguments(self._client.legacy_run.create,
                                                        create_run_dto=create_run_dto,
                                                        is_async=is_async)

        return self._execute_with_project_arguments(self._client.run.patch,
                                                    run_id=run_id,
                                                    create_run_dto=create_run_dto,
                                                    is_async=is_async)

    def get_child_runs(self, parent_run_id, root_run_id, recursive=False, _filter_on_server=False, **kwargs):
        """
        Get child runs by parent_run_id
        :param str parent_run_id: parent_run_id(required)
        :param str root_run_id: optimization id for hierarchy(required)
        :param bool recursive: fetch grandchildren and further descendants(required)
        :return: list of dictionary whose keys are property of ~_restclient.models.RunDto
        """
        order_expression = [ORDER_BY_STARTTIME_EXPRESSION]
        filter_expression = self._get_run_filter_expr(**kwargs) if _filter_on_server else None
        if recursive:
            root_filter = 'RootRunId eq {0}'.format(root_run_id)
            full_filter = and_join([root_filter, filter_expression]) if _filter_on_server else root_filter
            run_dtos = self._execute_with_project_arguments(self._client.run.list,
                                                            orderby=order_expression,
                                                            filter=full_filter,
                                                            is_paginated=True)
            if not _filter_on_server:
                run_dtos = self._client_filter(run_dtos, **kwargs)
            run_hierarchy = Tree(run_dtos)
            return run_hierarchy.get_subtree_dtos(parent_run_id)
        else:
            route = (self._client.legacy_run.get_child if self.api_route ==
                     RunHistoryClient.OLD_ROUTE else self._client.run.get_child)
            run_dtos = self._execute_with_project_arguments(route,
                                                            run_id=parent_run_id,
                                                            orderby=order_expression,
                                                            filter=filter_expression,
                                                            is_paginated=True)
            return run_dtos if _filter_on_server else self._client_filter(run_dtos, **kwargs)

    def create_child_run(self, parent_run_id, run_id, script_name=None, target=None, run_name=None, is_async=False):
        """
        Create a child run
        :param str parent_run_id: parent_run_id(required)
        :param str run_id: run_id(required)
        :param str script_name: script name
        :param str target: run target
        :param str run_name: run_name
        :param is_async bool: execute request asynchronously
        :return:
            If is_async parameter is True,
            the request is called asynchronously.
            The method returns azureml._async.AsyncTask object
            If parameter is_async is False or missing,
            return ~_restclient.models.RunDto
        """
        create_run_dto = CreateRunDto(run_id=run_id,
                                      parent_run_id=parent_run_id,
                                      script_name=script_name,
                                      target=target,
                                      name=run_name,
                                      status='NotStarted')

        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_project_arguments(self._client.legacy_run.create_child,
                                                        run_id=parent_run_id,
                                                        new_child_run=create_run_dto,
                                                        is_async=is_async)
        else:
            return self._execute_with_project_arguments(self._client.run.patch,
                                                        run_id=run_id,
                                                        create_run_dto=create_run_dto,
                                                        is_async=is_async)

    def get_runstatus(self, run_id, is_async=False):
        """
        Get status details of a run by its run_id
        :param str run_id:  (required)
        :param is_async bool: execute request asynchronously
        :return:
            If is_async parameter is True,
            the request is called asynchronously.
            The method returns azureml._async.AsyncTask object
            If parameter is_async is False or missing,
            return ~_restclient.models.RunDetailsDto
        """
        if self.api_route == RunHistoryClient.OLD_ROUTE:
            func = self._client.legacy_run.get_status
        else:
            func = self._client.run.get_details
        return self._execute_with_project_arguments(func, run_id=run_id, is_async=is_async)

    def get_run(self, run_id, is_async=False):
        """
        Get detail of a run by its run_id
        :param str run_id:  (required)
        :param is_async bool: execute request asynchronously
        :return:
            If is_async parameter is True,
            the request is called asynchronously.
            The method returns azureml._async.AsyncTask object
            If parameter is_async is False or missing,
            return ~_restclient.models.RunDto
        """
        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_project_arguments(
                self._client.legacy_run.get, run_id=run_id, is_async=is_async)

        return self._execute_with_project_arguments(
            self._client.run.get, run_id=run_id, is_async=is_async)

    def get_runs(self, last=0, pagesize=0, _filter_on_server=False, **kwargs):
        """
        Get detail of all runs of an experiment
        :param int last: the number of latest runs to return (optional)
        :param int pagesize: the number of item in each page returned (optional)
        :return: a generator of ~_restclient.models.RunDto
        """
        order_expression = [ORDER_BY_STARTTIME_EXPRESSION]
        pagesize = DEFAULT_PAGE_SIZE if pagesize < 1 else pagesize
        top = last if last < pagesize else pagesize
        filter_expression = self._get_run_filter_expr(**kwargs) if _filter_on_server else None

        route = (self._client.legacy_run.list if self.api_route ==
                 RunHistoryClient.OLD_ROUTE else self._client.run.list)
        run_dtos = self._execute_with_project_arguments(route,
                                                        total_count=last,
                                                        orderby=order_expression,
                                                        top=top,
                                                        filter=filter_expression,
                                                        is_paginated=True)

        return run_dtos if _filter_on_server else self._client_filter(run_dtos, **kwargs)

    def get_runs_by_run_ids(self, run_ids=None):
        """
        Get detail of all runs of an experiment
        :param int last: the number of latest runs to return (optional)
        :param int pagesize: the number of item in each page returned (optional)
        :return: a generator of ~_restclient.models.RunDto
        """
        order_expression = [ORDER_BY_RUNID_EXPRESSION]
        kwargs = {'orderby': order_expression, 'is_paginated': True}

        if run_ids is not None:
            kwargs['filter'] = get_run_ids_filter_expression(run_ids)

        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_project_arguments(self._client.legacy_run.list, **kwargs)

        return self._execute_with_project_arguments(self._client.run.list, **kwargs)

    def get_metrics_by_run_ids(self, run_ids=None, custom_headers=None, orderby=None):
        """
        Get run_metrics of multiple runs
        :param str run_ids:  run ids(optional)
        :param dict custom_headers: custom headers as dictionary(optional)
        :param list str orderby: sorted by a property(optional), for example: property_name asc(or desc)
        :return: a generator of ~_restclient.models.RunMetricDto
        """
        kwargs = {'custom_headers': custom_headers, 'is_paginated': True}
        if run_ids is not None:
            kwargs['filter'] = get_run_ids_filter_expression(run_ids)

        kwargs['orderby'] = orderby if orderby is not None else [ORDER_BY_RUNID_EXPRESSION]

        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_project_arguments(self._client.legacy_runmetric.list, **kwargs)

        return self._execute_with_project_arguments(self._client.run_metric.list, **kwargs)

    def get_metrics(self, run_id=None):
        """
        Get run_metrics of an experiment
        :param str run_id:  (optional)
        :return: a generator of ~_restclient.models.RunMetricDto
        """
        kwargs = {'is_paginated': True}
        if run_id is not None:
            kwargs['filter'] = '{}{}'.format(RUN_ID_EXPRESSION, run_id)

        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_project_arguments(self._client.legacy_runmetric.list, **kwargs)

        return self._execute_with_project_arguments(self._client.run_metric.list, **kwargs)

    def get_metrics_by_runs(self, run_ids=None):
        """
        Get run_metrics of multiple runs
        :param str run_ids:  (optional)
        :return: list of dictionary whose keys are property of ~_restclient.models.RunMetricDto
        """
        self._logger.warning("get_metrics_by_runs is deprecated, please use get_metrics_by_run_ids")
        if isinstance(run_ids, list):
            filter = get_run_ids_filter_expression(run_ids)
            order_expression = [ORDER_BY_RUNID_EXPRESSION]
            return self._combine_with_project_paginated_dto(self._client.runmetric.list,
                                                            filter=filter, orderby=order_expression)

        return self._combine_with_project_paginated_dto(self._client.runmetric.list)

    def post_runmetrics(self, run_id, run_metric_dto, is_async=False):
        """
        Post run_metrics of one run
        :param str run_ids: run_id
        :param run_metric_dto run_metric_dto: a ~_restclient.models.RunMetricDto object
        :param is_async bool: execute request asynchronously
        :return:
            If is_async parameter is True,
            the request is called asynchronously.
            The method returns azureml._async.AsyncTask object
            If parameter is_async is False or missing,
            return None
        """
        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_project_arguments(self._client.legacy_runmetric.post,
                                                        run_id=run_id,
                                                        run_metric_dto=run_metric_dto,
                                                        is_async=is_async)

        return self._execute_with_project_arguments(self._client.run_metric.post,
                                                    run_id=run_id,
                                                    run_metric_dto=run_metric_dto,
                                                    is_async=is_async)

    def update_run(self, run_id, modify_run_dto, is_async=False):
        """
        Update a run to the run history client
        :param str run_id:  (required)
        :param ~_restclient.models.ModifyRunDto modify_run_dto: modified run object(required)
        :param is_async bool: execute request asynchronously
        :return:
            If is_async parameter is True,
            the request is called asynchronously.
            The method returns azureml._async.AsyncTask object
            If parameter is_async is False or missing,
            return: ~_restclient.models.RunDto
        """
        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_project_arguments(self._client.legacy_run.update,
                                                        run_id=run_id,
                                                        modify_run_dto=modify_run_dto,
                                                        is_async=is_async)

        return self._execute_with_project_arguments(self._client.run.update,
                                                    run_id=run_id,
                                                    modify_run_dto=modify_run_dto,
                                                    is_async=is_async)

    def patch_run(self, run_id, create_run_dto, is_async=False):
        """
        Patch a run to the run history client
        :param str run_id:  (required)
        :param create_run_dto: a new run object(required)
        :type ~_restclient.models.CreateRunDto
        :param is_async bool: execute request asynchronously
        :return:
            If is_async parameter is True,
            the request is called asynchronously.
            The method returns azureml._async.AsyncTask object
            If parameter is_async is False or missing,
            return: ~_restclient.models.RunDto
        """
        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_project_arguments(self._client.legacy_run.patch,
                                                        run_id=run_id,
                                                        modify_run_dto=create_run_dto,
                                                        is_async=is_async)

        return self._execute_with_project_arguments(self._client.run.patch,
                                                    run_id=run_id,
                                                    create_run_dto=create_run_dto,
                                                    is_async=is_async)

    def modify_run(self, create_run_dto, is_async=False):
        """
        Patch or create a run to the run history client,
        :param create_run_dto: a new run object(required)
        :type ~_restclient.models.CreateRunDto
        :param is_async bool: execute request asynchronously
        :return:
            If is_async parameter is True,
            the request is called asynchronously.
            The method returns azureml._async_task.AsyncTask object
            If parameter is_async is False or missing,
            return: ~_restclient.models.RunDto
        """
        if self.api_route == RunHistoryClient.OLD_ROUTE:
            return self._execute_with_project_arguments(self._client.legacy_run.add_or_modify,
                                                        create_run_dto=create_run_dto,
                                                        is_async=is_async)

        return self._execute_with_project_arguments(self._client.run.patch,
                                                    run_id=create_run_dto.run_id,
                                                    create_run_dto=create_run_dto,
                                                    is_async=is_async)

    _run_filter_mapping = {
        'tags': get_filter_run_tags,
        'properties': get_filter_run_properties,
        'runtype': get_filter_run_type,
        'created': get_filter_run_created_after
    }

    def _get_run_filter_expr(self, **kwargs):
        exprs = []
        for filter_type, filter_val in kwargs.items():
            if filter_val is None:
                self._logger.debug("Skipping filter %s for None val", filter_type)
                continue
            filter_func = RunHistoryClient._run_filter_mapping.get(filter_type, None)
            if filter_func is None:
                self._logger.warning("Received unknown filter type: {0} on {1}".format(filter_type, filter_val))
            else:
                self._logger.debug("Getting filter %s for %s", filter_func, filter_val)
                exprs.append(filter_func(filter_val))
        return None if len(exprs) < 1 else and_join(exprs)

    def _filter_run_on_created_after(run_dto, created_after):
        return run_dto.created_utc >= created_after

    def _filter_run_on_type(run_dto, type):
        return run_dto.run_type == type

    def _filter_run_on_tags(run_dto, tags):
        if isinstance(tags, six.text_type) and tags in run_dto.tags.keys():
            return True
        elif isinstance(tags, dict):
            if set(tags.items()).issubset(run_dto.tags.items()):
                return True
        return False

    def _filter_run_on_props(run_dto, props):
        if isinstance(props, six.text_type) and props in run_dto.properties.keys():
            return True
        elif isinstance(props, dict):
            if set(props.items()).issubset(run_dto.properties.items()):
                return True
        return False

    _run_client_filter_mapping = {
        'tags': _filter_run_on_tags,
        'properties': _filter_run_on_props,
        'runtype': _filter_run_on_type,
        'created': _filter_run_on_created_after
    }

    def _client_filter(self, run_dtos, **kwargs):
        filter_funcs = {}
        for filter_type, filter_val in kwargs.items():
            if filter_val is None:
                self._logger.debug("Skipping filter %s for None val", filter_type)
                continue

            filter_func = RunHistoryClient._run_client_filter_mapping.get(filter_type, None)
            if filter_func is None:
                self._logger.warning("Received unknown filter type: {0} on {1}".format(filter_type, filter_val))
            else:
                self._logger.debug("Getting filter %s for %s", filter_func, filter_val)
                filter_funcs[filter_func] = filter_val

        for run_dto in run_dtos:
            skip = False
            for func, val in filter_funcs.items():
                self._logger.debug("client filtering %s on %s", run_dto, val)
                if not func(run_dto, val):
                    skip = True
            if not skip:
                yield run_dto

    def _prepare_experiment(self):
        run_id = get_new_id()
        create_run_dto = CreateRunDto(run_id=run_id,
                                      hidden=True)
        self.create_run(run_id=run_id, create_run_dto=create_run_dto)
        self._logger.debug("Created run  with id {} to prepare experiment".format(run_id))
