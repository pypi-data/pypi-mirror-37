# Copyright 2017 Okera Inc.

from __future__ import absolute_import

import datetime
import os
import random
import pytz

from decimal import Decimal
from collections import OrderedDict
from okera._util import get_logger_and_init_null
from okera._thrift_api import (
    TGetDatabasesParams, TGetTablesParams, TNetworkAddress,
    TPlanRequestParams, TRequestType,
    TExecDDLParams, TExecTaskParams, TFetchParams, TRecordFormat, TTypeId,
    CerebroRecordServicePlanner, RecordServiceWorker)
from okera._thrift_util import (
    create_socket, get_transport, TTransportException, TBinaryProtocol,
    PlannerClient, WorkerClient, KERBEROS_NOT_ENABLED_MSG, SOCKET_READ_ZERO)
from .concurrency import (BaseBackgroundTask,
                          ConcurrencyController,
                          default_max_client_process_count)

_log = get_logger_and_init_null(__name__)

""" Context for this user session."""
class OkeraContext():
    def __init__(self, application_name, tz=pytz.utc):
        _log.debug('Creating okera context')
        self.__auth = None
        self.__service_name = None
        self.__token = None
        self.__host_override = None
        self.__user = None
        self.__name = application_name
        self.__configure()
        self.__tz = tz

    def enable_kerberos(self, service_name, host_override=None):
        """Enable kerberos based authentication.

        Parameters
        ----------
        service_name : str
            Authenticate to a particular `okera` service principal. This is typically
            the first part of the 3-part service principal (SERVICE_NAME/HOST@REALM).

        host_override : str, optional
            If set, the HOST portion of the server's service principal. If not set,
            then this is the resolved DNS name of the service being connected to.

        Returns
        -------
        OkeraContext
            Returns this object.
        """

        if not service_name:
            raise ValueError("Service name must be specified.")
        self.__auth = 'GSSAPI'
        self.__service_name = service_name
        self.__host_override = host_override
        self.__user = None
        _log.debug('Enabled kerberos')
        return self

    def enable_token_auth(self, token_str=None, token_file=None):
        """Enables token based authentication.

        Parameters
        ----------
        token_str : str, optional
            Authentication token to use.
        token_file : str, optional
            File containing token to use.

        Returns
        -------
        OkeraContext
            Returns this object.
        """

        if not token_str and not token_file:
            raise ValueError("Must specify token_str or token_file")
        if token_str and token_file:
            raise ValueError("Cannot specify both token_str token_file")

        if token_file:
            with open(os.path.expanduser(token_file), 'r') as t:
                token_str = t.read()
        self.__configure_token(token_str.strip())
        _log.debug('Enabled token auth')
        return self

    def disable_auth(self):
        """ Disables authentication.

        Returns
        -------
        OkeraContext
            Returns this object.
        """
        self.__auth = None
        self.__token = None
        self.__service_name = None
        self.__host_override = None
        self.__user = None
        _log.debug('Disabled auth')
        return self

    def get_auth(self):
        """ Returns the configured auth mechanism. None if no auth is enabled."""
        return self.__auth

    def get_token(self):
        """ Returns the token string. Note that logging this should be done with care."""
        return self.__token

    def get_name(self):
        """ Returns name of this application. This is recorded for diagnostics on
            the server.
        """
        return self.__name

    def _get_user(self):
        """ Returns the user name. This is ignored if authentication is enabled. """
        return self.__user

    def get_timezone(self):
        return self.__tz

    def connect(self, host='localhost', port=12050, timeout=None):
        """Get a connection to an ODAS cluster. This connects to the planner service.

        Parameters
        ----------
        host : str or list of hostnames
            The hostname for the planner. If a list is specified, picks a planner at
            random.
        port : int, optional
            The port number for the planner. The default is 12050.
        timeout : int, optional
            Connection timeout in seconds. Default is no timeout.

        Returns
        -------
        PlannerConnection
            Handle to a connection. Users should call `close()` when done.
        """

        host, port = self.__pick_host(host, port)

        # Convert from user names to underlying transport names
        auth_mechanism = self.__get_auth()

        _log.debug('Connecting to planner %s:%s with %s authentication '
                   'mechanism', host, port, auth_mechanism)
        sock = create_socket(host, port, timeout, False, None)
        transport = None
        try:
            transport = get_transport(sock, host, auth_mechanism, self.__service_name,
                                      None, None, self.__token, self.__host_override)
            transport.open()
            protocol = TBinaryProtocol(transport)
            service = _ThriftService(PlannerClient(CerebroRecordServicePlanner, protocol))
            planner = PlannerConnection(service, self)
            planner.set_application(self.__name)
            return planner
        except (TTransportException, IOError) as e:
            sock.close()
            if transport:
                transport.close()
            self.__handle_transport_exception(e)
            raise e
        except:
            sock.close()
            if transport:
                transport.close()
            raise

    def connect_worker(self, host='localhost', port=13050, timeout=None):
        """Get a connection to ODAS worker.

        Most users should not need to call this API directly.

        Parameters
        ----------
        host : str or list of hostnames
            The hostname for the worker. If a list is specified, picks a worker at
            random.
        port : int, optional
            The port number for the worker. The default is 13050.
        timeout : int, optional
            Connection timeout in seconds. Default is no timeout.

        Returns
        -------
        WorkerConnection
            Handle to a worker connection. Users must call `close()` when done.
        """
        return self._connect_worker(host, port, timeout=timeout)

    def _connect_worker(self, host, port, timeout=None, options=None):
        host, port = self.__pick_host(host, port, options)

        auth_mechanism = self.__get_auth()
        _log.debug('Connecting to worker %s:%s with %s authentication '
                   'mechanism', host, port, auth_mechanism)

        sock = create_socket(host, port, timeout, False, None)
        transport = None
        try:
            transport = get_transport(sock, host, auth_mechanism, self.__service_name,
                                      None, None, self.__token, self.__host_override)
            transport.open()
            protocol = TBinaryProtocol(transport)
            service = _ThriftService(WorkerClient(RecordServiceWorker, protocol))
            worker = WorkerConnection(service, self)
            worker.set_application(self.__name)
            return worker
        except (TTransportException, IOError) as e:
            sock.close()
            if transport:
                transport.close()
            self.__handle_transport_exception(e)
            raise e
        except:
            sock.close()
            if transport:
                transport.close()
            raise

    @staticmethod
    def __pick_host(host, port, options=None):
        """
        Returns a host, port from the input. host can be a string or a list of strings.
        If it is a list, a host is picked from the list. If the host string contains the
        port that port is used, otherwise, the port argument is used.
        """
        if not host:
            raise ValueError("host must be specified")

        if isinstance(host, list):
            chosen_host = host[0]
            if isinstance(chosen_host, TNetworkAddress):
                # With this option, we want to pin a host instead of picking a random one.

                if options and 'PIN_HOST' in options:
                    host.sort(key = lambda v: v.hostname)
                    chosen_host = host[0]
                else:
                    chosen_host = random.choice(host)
                host = chosen_host.hostname
                port = chosen_host.port
            elif isinstance(chosen_host, str):
                if options and 'PIN_HOST' in options:
                    host.sort()
                    host = host[0]
                else:
                    host = random.choice(host)
                host = chosen_host
            else:
                raise ValueError("host list must be TNetworkAddress objects or strings.")

        if isinstance(host, str):
            parts = host.split(':')
            if len(parts) == 2:
                host = parts[0]
                port = int(parts[1])
            elif len(parts) == 1:
                host = parts[0]
                if port is None:
                    raise ValueError("port must be specified")
            else:
                raise ValueError("Invalid host: %s " % host)
        else:
            raise ValueError("Invalid host: %s" % host)
        return host, port

    def __configure(self):
        """ Configures the context based on system wide settings"""
        home = os.path.expanduser("~")
        token_file = os.path.join(home, '.cerebro', 'token')
        if os.path.exists(token_file):
            # TODO: we could catch this exception and go on but having this file be
            # messed up here is likely something to fix ASAP.
            with open(token_file, 'r') as t:
                self.__configure_token(t.read().strip())
            _log.info("Configured token auth with token in home directory.")

    def __configure_token(self, token):
        # Valid authentication tokens contain '.' in them, either an Okera token or a JWT
        # token. For API convenience, we use the token value to mean user (plain text)
        # when run against unauthenticated servers.
        if '.' in token:
            self.__token = token
            self.__auth = 'TOKEN'
            self.__service_name = 'cerebro'
            self.__user = None
        else:
            self.__token = None
            self.__auth = None
            self.__user = token
        self.__host_override = None

    def __handle_transport_exception(self, e):
        """ Maps transport layer exceptions to better user facing ones. """
        if self.__auth and e.message == SOCKET_READ_ZERO:
            e.message = "Server did not respond to authentication handshake. " + \
                        "Ensure server has authentication enabled."
        elif not self.__auth and e.message == SOCKET_READ_ZERO:
            e.message = "Client does not have authentication enabled but it appears " + \
                        "the server does. Enable client authentication."
        elif self.__auth == 'GSSAPI' and KERBEROS_NOT_ENABLED_MSG in e.message:
            e.message = "Client is authenticating with kerberos but kerberos is not " + \
                        "enabled on the server."
        raise e

    def __get_auth(self):
        """ Canonicalizes user facing auth names to transport layer ones """
        auth_mechanism = self.__auth
        if not auth_mechanism:
            auth_mechanism = 'NOSASL'
        if auth_mechanism == 'TOKEN':
            auth_mechanism = 'DIGEST-MD5'
        return auth_mechanism

class _ThriftService():
    """ Wrapper around a thrift service client object """
    def __init__(self, thrift_client, retries=3):
        self.client = thrift_client
        self.retries = retries

    def close(self):
        # pylint: disable=protected-access
        _log.debug('close_service: client=%s', self.client)
        self.client._iprot.trans.close()

    def reconnect(self):
        # pylint: disable=protected-access
        _log.debug('reconnect: client=%s', self.client)
        self.client._iprot.trans.close()
        self.client._iprot.trans.open()

class PlannerConnection():
    """A connection to an ODAS planner. """

    def __init__(self, thrift_service, ctx):
        self.service = thrift_service
        self.ctx = ctx
        _log.debug('PlannerConnection(service=%s)', self.service)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the session and server connection."""
        _log.debug('Closing Planner connection')
        self.service.close()

    def _reconnect(self):
        self.service.reconnect()

    def _underlying_client(self):
        """ Returns the underlying thrift client. Exposed for internal use. """
        return self.service.client

    def get_protocol_version(self):
        """Returns the RPC API version of the server."""
        return self.service.client.GetProtocolVersion()

    def set_application(self, name):
        """Sets the name of this session. Used for logging purposes on the server."""
        self.service.client.SetApplication(name)

    def list_databases(self):
        """Lists all the databases in the catalog

        Returns
        -------
        list(str)
            List of database names.

        Examples
        --------
        >>> import okera
        >>> ctx = okera.context()
        >>> with ctx.connect(host = 'localhost', port = 12050) as conn:
        ...     dbs = conn.list_databases()
        ...     'okera_sample' in dbs
        True
        """

        request = TGetDatabasesParams()
        if self.ctx._get_user():
            request.requesting_user = self.ctx._get_user()
        result = self.service.client.GetDatabases(request)
        dbs = []
        for db  in result.databases:
            dbs.append(db.name[0])
        return dbs

    def list_dataset_names(self, db, filter=None):
        """ Returns the names of the datasets in this db

        Parameters
        ----------
        db : str
            Name of database to return datasets in.
        filter : str, optional
            Substring filter on names to of datasets to return.

        Returns
        -------
        list(str)
            List of dataset names.

        Examples
        --------
        >>> import okera
        >>> ctx = okera.context()
        >>> with ctx.connect(host = 'localhost', port = 12050) as conn:
        ...     datasets = conn.list_dataset_names('okera_sample')
        ...     datasets
        ['okera_sample.sample', 'okera_sample.users']
        """
        request = TGetTablesParams()
        request.database = [db]
        request.filter = filter
        if self.ctx._get_user():
            request.requesting_user = self.ctx._get_user()
        tables = self.service.client.GetTables(request).tables
        result = []
        for t in tables:
            result.append(db + '.' + t.name)
        return result

    def list_datasets(self, db, filter=None):
        """ Returns the datasets in this db

        Parameters
        ----------
        db : str
            Name of database to return datasets in.
        filter : str, optional
            Substring filter on names to of datasets to return.

        Returns
        -------
        obj
            Thrift dataset objects.
        Note
        -------
        This API is subject to change and the returned object may not be backwards
        compatible.
        """

        request = TGetTablesParams()
        request.database = [db]
        request.filter = filter
        if self.ctx._get_user():
            request.requesting_user = self.ctx._get_user()
        tables = self.service.client.GetTables(request)
        return tables

    def plan(self, request, max_task_count=None, requesting_user=None):
        """ Plans the request to read from CDAS
        Parameters
        ----------
        request : str, required
            Name of dataset or SQL statement to plan scan for.
        requesting_user : str, optional
            Name of user to request plan for, if different from
            the current user.

        Returns
        -------
        object
            Thrift serialized plan object.

        Note
        -------
        This API is subject to change and the returned object may not be backwards
        compatible.
        """

        if not request:
            raise ValueError("request must be specified.")

        params = TPlanRequestParams()
        params.request_type = TRequestType.Sql
        if max_task_count:
            params.max_tasks = max_task_count
        if requesting_user:
            params.requesting_user = requesting_user
        elif self.ctx._get_user():
            params.requesting_user = self.ctx._get_user()

        request = request.strip()
        if request.lower().startswith('select '):
            _log.debug('Planning request for query: %s', request)
            params.sql_stmt = request
        else:
            _log.debug('Planning request to read dataset: %s', request)
            params.sql_stmt = "SELECT * FROM " + request
        plan = self.service.client.PlanRequest(params)
        _log.debug('Plan complete. Number of tasks: %d', len(plan.tasks))
        return plan

    def execute_ddl(self, sql):
        # pylint: disable=line-too-long
        """ Execute a DDL statement against the server.

        Parameters
        ----------
        sql : str
            DDL statement to run

        Returns
        -------
        list(list(str))
            Returns the result as a table.

        Examples
        --------
        >>> import okera
        >>> ctx = okera.context()
        >>> with ctx.connect(host = 'localhost', port = 12050) as conn:
        ...     result = conn.execute_ddl('describe okera_sample.users')
        ...     result
        [['uid', 'string', 'Unique user id'], ['dob', 'string', 'Formatted as DD-month-YY'], ['gender', 'string', ''], ['ccn', 'string', 'Sensitive data, should not be accessible without masking.']]
        """
        # pylint: enable=line-too-long

        if not sql:
            raise ValueError("Must specify sql string to execute_ddl")
        request = TExecDDLParams()
        request.ddl = sql
        if self.ctx._get_user():
            request.requesting_user = self.ctx._get_user()
        response = self.service.client.ExecuteDDL2(request)
        return response.tabular_result

    def execute_ddl_table_output(self, sql):
        """ Execute a DDL statement against the server.

        Parameters
        ----------
        sql : str
            DDL statement to run

        Returns
        -------
        PrettyTable
            Returns the result as a table object.

        Examples
        --------
        >>> import okera
        >>> ctx = okera.context()
        >>> with ctx.connect(host = 'localhost', port = 12050) as conn:
        ...     result = conn.execute_ddl_table_output('describe okera_sample.users')
        ...     print(result)
        +--------+--------+-----------------------------------------------------------+
        |  name  |  type  |                          comment                          |
        +--------+--------+-----------------------------------------------------------+
        |  uid   | string |                       Unique user id                      |
        |  dob   | string |                  Formatted as DD-month-YY                 |
        | gender | string |                                                           |
        |  ccn   | string | Sensitive data, should not be accessible without masking. |
        +--------+--------+-----------------------------------------------------------+
        """
        from prettytable import PrettyTable

        if not sql:
            raise ValueError("Must specify sql string to execute_ddl")
        request = TExecDDLParams()
        request.ddl = sql
        if self.ctx._get_user():
            request.requesting_user = self.ctx._get_user()
        response = self.service.client.ExecuteDDL2(request)
        if not response.col_names:
            return None

        t = PrettyTable(response.col_names)
        for row in response.tabular_result:
            t.add_row(row)
        return t

    def scan_as_pandas(self,
                       request,
                       max_records=None,
                       max_client_process_count=default_max_client_process_count(),
                       max_task_count=None,
                       requesting_user=None,
                       options=None,
                       ignore_errors=False):
        """Scans data, returning the result for pandas.

        Parameters
        ----------
        request : string, required
            Name of dataset or SQL statement to scan.
        max_records : int, optional
            Maximum number of records to return. Default is unlimited.
        options : dictionary, optional
            Optional key/value configs to specify to the request. Note that these
            options are not guaranteed to be backwards compatible.

        Returns
        -------
        pandas DataFrame
            Data returned as a pandas DataFrame object

        Examples
        --------
        >>> import okera
        >>> ctx = okera.context()
        >>> with ctx.connect(host = 'localhost', port = 12050) as conn:
        ...     pd = conn.scan_as_pandas('select * from okera_sample.sample')
        ...     print(pd)
                                       record
        0      b'This is a sample test file.'
        1  b'It should consist of two lines.'
        """
        import pandas
        plan = self.plan(request,
                         max_task_count=max_task_count,
                         requesting_user=requesting_user)
        self._ensure_serialization_support(plan)

        concurrency_ctl = self._get_concurrency_controller_for_plan(
            plan, max_client_process_count)

        for task in plan.tasks:
            _log.debug('Executing task %s', str(task.task_id))
            concurrency_ctl.enqueueTask(PandasScanTask(self.ctx,
                                                       plan.hosts,
                                                       task,
                                                       max_records,
                                                       options))

        result_list = self._start_and_wait_for_results(concurrency_ctl,
                                                       len(plan.tasks),
                                                       limit=max_records,
                                                       is_pandas=True,
                                                       ignore_errors=ignore_errors)
        if not result_list:
            col_names = []
            for col in plan.schema.cols:
                col_names.append(col.name)
            return pandas.DataFrame(columns=col_names)
        else:
            return pandas.concat(result_list).head(max_records)

    def scan_as_json(self,
                     request,
                     max_records=None,
                     max_client_process_count=default_max_client_process_count(),
                     max_task_count=None,
                     requesting_user=None,
                     ignore_errors=False):
        # pylint: disable=line-too-long
        """Scans data, returning the result in json format.

        Parameters
        ----------
        request : string, required
            Name of dataset or SQL statement to scan.
        max_records : int, optional
            Maximum number of records to return. Default is unlimited.

        Returns
        -------
        list(obj)
            Data returned as a list of JSON objects

        Examples
        --------
        >>> import okera
        >>> ctx = okera.context()
        >>> with ctx.connect(host = 'localhost', port = 12050) as conn:
        ...     data = conn.scan_as_json('okera_sample.sample')
        ...     data
        [{'record': 'This is a sample test file.'}, {'record': 'It should consist of two lines.'}]
        """
        # pylint: enable=line-too-long

        plan = self.plan(request,
                         max_task_count=max_task_count,
                         requesting_user=requesting_user)
        self._ensure_serialization_support(plan)

        concurrency_ctl = self._get_concurrency_controller_for_plan(
            plan, max_client_process_count)

        if len(plan.tasks) <= 0:
            return []

        for task in plan.tasks:
            _log.debug('Executing task %s', str(task.task_id))
            concurrency_ctl.enqueueTask(JsonScanTask(self.ctx,
                                                    plan.hosts,
                                                    task,
                                                    max_records))

        res = self._start_and_wait_for_results(concurrency_ctl,
                                               len(plan.tasks),
                                               limit=max_records,
                                               ignore_errors=ignore_errors)
        if max_records is not None:
            return res[:max_records]
        return res

    @staticmethod
    def _get_concurrency_controller_for_plan(plan, max_client_process_count):
        worker_count = min(max_client_process_count, len(plan.tasks))
        return ConcurrencyController(worker_count=worker_count)

    @staticmethod
    def _calculate_limit(current_limit, results, is_pandas):
        if current_limit is None:
            return None
        if is_pandas:
            if len(results) == 0:
                return current_limit
            return max(current_limit-len(results[0].index), 0)
        return max(current_limit-len(results), 0)

    @staticmethod
    def _start_and_wait_for_results(concurrency_ctl,
                                    task_count,
                                    limit=None,
                                    is_pandas=False,
                                    ignore_errors=False):
        results = []
        if not task_count:
            return results
        try:
            task_result_count = 0
            is_completed = False
            # We're setting the limit value into a shared dict that is handed
            # to all async tasks.  The main thread (this function) is responsible
            # for updating the value as records are received.  The async tasks
            # will read this `limit` value from the dict and pass it as the
            # `max_records` param to the worker.  As records are received in the
            # main thread, the `limit` value will decrease until it is zero, at
            # which point the remaining async tasks will immediately return
            # with empty results.
            concurrency_ctl.metrics_dict['limit'] = limit

            # All default values need to be set prior to calling start().  This is
            # because there will be a delay when setting any shared value between
            # processes because the values are cached in each process.
            concurrency_ctl.start()

            while not is_completed:
                res = concurrency_ctl.output_queue.get()
                if res is not None:
                    task_result_count += 1
                    limit = PlannerConnection._calculate_limit(limit, res, is_pandas)
                    results.extend(res)
                    if task_result_count == task_count:
                        is_completed = True
                    concurrency_ctl.metrics_dict['limit'] = limit

            if not ignore_errors and concurrency_ctl.errors_queue.qsize():
                print('One or more errors occurred while processing this query:')
                while concurrency_ctl.errors_queue.qsize():
                    err = concurrency_ctl.errors_queue.get()
                    print('{0}'.format(err))
                    raise err
        finally:
            concurrency_ctl.stop()

        return results

    @staticmethod
    def _ensure_serialization_support(plan):
        if not plan.supported_result_formats or \
                TRecordFormat.ColumnarNumPy not in plan.supported_result_formats:
            raise IOError("PyOkera requires the server to support the " +
                          "`ColumnarNumPy` serialization format. Please upgrade the " +
                          "server to at least 0.8.1.")

class WorkerConnection():
    """A connection to a CDAS worker. """

    def __init__(self, thrift_service, ctx):
        self.service = thrift_service
        self.ctx = ctx
        _log.debug('WorkerConnection(service=%s)', self.service)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the session and server connection."""
        _log.debug('Closing Worker connection')
        self.service.close()

    def _reconnect(self):
        self.service.reconnect()

    def get_protocol_version(self):
        """Returns the RPC API version of the server."""
        return self.service.client.GetProtocolVersion()

    def set_application(self, name):
        """Sets the name of this session. Used for logging purposes on the server."""
        self.service.client.SetApplication(name)

    def exec_task(self, task, max_records=None):
        """ Executes a task to begin scanning records.

        Parameters
        ----------
        task : obj
            Description of task. This is the result from the planner's plan() call.
        max_records: int, optional
            Maximum number of records to return for this task. Default is unlimited.

        Returns
        -------
        object
            Handle for this task. Used in subsequent API calls.
        object
            Schema for records returned from this task.
        """
        request = TExecTaskParams()
        request.task = task.task
        request.limit = max_records
        request.fetch_size = 20000
        request.record_format = TRecordFormat.ColumnarNumPy
        result = self.service.client.ExecTask(request)
        return result.handle, result.schema

    def close_task(self, handle):
        """ Closes the task. """
        self.service.client.CloseTask(handle)

    def fetch(self, handle):
        """ Fetch the next batch of records for this task. """
        request = TFetchParams()
        request.handle = handle
        return self.service.client.Fetch(request)

def _columnar_batch_to_python(schema, columnar_records, num_records, ctx_tz=pytz.utc):
    # Issues with numpy, thrift and this function being perf optimized
    # pylint: disable=no-member
    # pylint: disable=protected-access
    # pylint: disable=too-many-locals
    import numpy
    cols = columnar_records.cols

    # Things we will return.
    col_names = []
    # Checks if any of the values in this batch are null. Handling NULL can be
    # noticeably slower, so skip it in bulk if possible.
    any_nulls = []
    is_nulls = [None] * len(cols)
    data = [None] * len(cols)

    # Go over each column and convert the binary data to python objects. This is very
    # perf sensitive.
    for col in range(0, len(cols)):
        buf = cols[col].data
        if isinstance(buf, str):
            buf = buf.encode()

        col_names.append(schema.cols[col].name)
        is_null = numpy.frombuffer(cols[col].is_null.encode(), dtype=numpy.bool)
        any_nulls.append(numpy.any(is_null))
        is_nulls[col] = is_null

        t = schema.cols[col].type.type_id
        if t == TTypeId.STRING or t == TTypeId.VARCHAR:
            off = 4 * num_records
            column = [numpy.nan] * num_records
            lens = numpy.frombuffer(buf[0: off], dtype=numpy.int32)
            if any_nulls[col]:
                for i in range(0, num_records):
                    if not is_null[i]:
                        length = lens[i]
                        column[i] = buf[off:off + length]
                        off += length
            else:
                for i in range(0, num_records):
                    length = lens[i]
                    column[i] = buf[off:off + length]
                    off += length
            data[col] = numpy.array(column, dtype=object)
        elif t == TTypeId.CHAR:
            off = 0
            column = [numpy.nan] * num_records
            length = schema.cols[col].type.len
            if any_nulls[col]:
                for i in range(0, num_records):
                    if not is_null[i]:
                        column[i] = buf[off:off + length]
                        off += length
            else:
                for i in range(0, num_records):
                    column[i] = buf[off:off + length]
                    off += length
            data[col] = numpy.array(column, dtype=object)
        elif t == TTypeId.BOOLEAN:
            data[col] = numpy.frombuffer(buf, dtype=numpy.bool)
        elif t == TTypeId.TINYINT:
            data[col] = numpy.frombuffer(buf, dtype=numpy.int8)
        elif t == TTypeId.SMALLINT:
            data[col] = numpy.frombuffer(buf, dtype=numpy.int16)
        elif t == TTypeId.INT:
            data[col] = numpy.frombuffer(buf, dtype=numpy.int32)
        elif t == TTypeId.BIGINT:
            data[col] = numpy.frombuffer(buf, dtype=numpy.int64)
        elif t == TTypeId.FLOAT:
            data[col] = numpy.frombuffer(buf, dtype=numpy.float32)
        elif t == TTypeId.DOUBLE:
            data[col] = numpy.frombuffer(buf, dtype=numpy.float64)
        elif t == TTypeId.TIMESTAMP_NANOS:
            dt = numpy.dtype([('millis', numpy.int64), ('nanos', numpy.int32)])
            values = numpy.frombuffer(buf, dtype=dt)
            millis = values['millis']
            column = [numpy.nan] * num_records
            for i in range(0, num_records):
                if not is_null[i]:
                    # TODO: use nanos?
                    column[i] = datetime.datetime.fromtimestamp(millis[i] / 1000.0,
                                                                ctx_tz)
            data[col] = column
        elif t == TTypeId.DECIMAL:
            if schema.cols[col].type.precision <= 9:
                values = numpy.frombuffer(buf, dtype=numpy.int32)
            elif schema.cols[col].type.precision <= 18:
                values = numpy.frombuffer(buf, dtype=numpy.int64)
            else:
                longs = numpy.frombuffer(buf, dtype=numpy.int64)
                values = [numpy.nan] * num_records
                for i in range(0, num_records):
                    values[i] = longs[i] + (longs[i + 1] << 64)
            column = [numpy.nan] * num_records
            scale = -schema.cols[col].type.scale
            for i in range(0, num_records):
                if not is_null[i]:
                    column[i] = Decimal(int(values[i])).scaleb(scale)
            data[col] = column
        else:
            raise RuntimeError("Unsupported type: " + TTypeId._VALUES_TO_NAMES[t])
    return col_names, data, any_nulls, is_nulls

def context(application_name=None):
    """ Gets the top level context object to use pyokera.

    Parameters
    ----------
    application_name : str, optional
        Name of this application. Used for logging and diagnostics.

    Returns
    -------
    OkeraContext
        Context object.

    Examples
    --------
    >>> import okera
    >>> ctx = okera.context()
    >>> ctx                                         # doctest: +ELLIPSIS
    <okera.odas.OkeraContext object at 0x...>
    """
    if not application_name:
        application_name = 'pyokera (%s)' % version()
    return OkeraContext(application_name)

def version():
    """ Returns version string of this library. """
    from . import __version__
    return __version__

class ScanTask(BaseBackgroundTask):
  def __init__(self, name, ctx, plan_hosts, task, max_records, options):
    BaseBackgroundTask.__init__(self, "ScanTask.{0}".format(name))
    self.ctx = ctx
    self.plan_hosts = plan_hosts
    self.task = task
    self.max_records = max_records
    self.options = options
    self.errors = []

  def __call__(self):
    results = []
    total = 0
    if self.max_records is not None and self.max_records <= 0:
        return results
    with self.ctx._connect_worker(self.plan_hosts, None, options=self.options) as worker:
        try:
            handle, schema = worker.exec_task(self.task, self.max_records)
            while True:
                fetch_result = worker.fetch(handle)
                assert fetch_result.record_format == TRecordFormat.ColumnarNumPy
                if fetch_result.num_records:
                    t_results = self.deserialize(schema,
                                                 fetch_result.columnar_records,
                                                 fetch_result.num_records)
                    if t_results:
                        results.extend(t_results)

                    total += fetch_result.num_records

                if fetch_result.done or (self.max_records and total >= self.max_records):
                    break
        except Exception as ex:
            self.errors.append(ex)
        finally:
            worker.close_task(handle)
    return results

  def deserialize(self, schema, columnar_records, num_records):
    '''Abstract definition to deserialize the returned dataset'''
    raise Exception('Invalid invocation of an abstract function: ' +
                    'BaseBackgroundTask::deserialize')

class JsonScanTask(ScanTask):
  def __init__(self, ctx, plan_hosts, task, max_records):
    ScanTask.__init__(self, "JsonScanTask", ctx, plan_hosts, task, max_records, None)

  def deserialize(self, schema, columnar_records, num_records):
    col_names, data, _, is_nulls = _columnar_batch_to_python(
        schema, columnar_records, num_records, self.ctx.get_timezone())
    num_cols = len(col_names)
    result = []
    # Go over each row and construct a python array as a row
    for r in range(0, num_records):
        row = [None] * num_cols
        for c in range(0, num_cols):
            if not is_nulls[c][r]:
                datum = data[c][r]
                row[c] = datum.decode('utf-8') if isinstance(datum, bytes) else datum
        result.append(dict(zip(col_names, row)))
    return result

class PandasScanTask(ScanTask):
  def __init__(self, ctx, plan_hosts, task, max_records, options):
    ScanTask.__init__(self, "PandasScanTask", ctx, plan_hosts, task, max_records, options)

  def deserialize(self, schema, columnar_records, num_records):
    import numpy
    import pandas
    result = []
    col_names, data, any_nulls, is_nulls = _columnar_batch_to_python(
        schema, columnar_records, num_records, self.ctx.get_timezone())
    df = pandas.DataFrame(OrderedDict(zip(col_names, data)))
    for c in range(0, len(col_names)):
        if not any_nulls[c] or df[col_names[c]].dtype == 'object':
            # Either no nulls, or objects are already handled.
            continue
        # Fix up nulls, replace with nan
        # TODO: this is not the cheapest
        df[col_names[c]] = df[col_names[c]].where(~is_nulls[c], other=numpy.nan)
    result.append(df)
    return result


Binary = memoryview
