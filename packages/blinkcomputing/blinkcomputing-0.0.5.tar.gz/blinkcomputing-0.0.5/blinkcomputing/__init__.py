# Copyright 2018 Blink Computing Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import requests
import time
from enum import IntEnum


logger = logging.getLogger(__name__)

class Connection:
    def __init__(self, cluster_id, coord_host, user_name, password, session=None,
                 stop_on_close=False, is_test=False):
        self._cluster_id = cluster_id
        self._coord_host = coord_host
        self._user_name = user_name
        self._password = password
        self._session = session
        self._stop_on_close = stop_on_close
        self._is_test = is_test

    def GetDbapiConnection(self):
        import impala.dbapi
        return impala.dbapi.connect(
            host=self._coord_host, use_ssl=True, auth_mechanism='PLAIN', user=self._user_name,
            password=self._password)

    def GetIbisConnection(self):
        import ibis.impala
        return ibis.impala.connect(
            host=self._coord_host, port=21050, hdfs_client=None, use_ssl=True,
            auth_mechanism='PLAIN', user=self._user_name, password=self._password)

    def Close(self):
        if not self._stop_on_close:
            return
        _StopCluster(self._session, self._cluster_id, self._is_test)

class Error(Exception):
    def __init__(self, msg):
        self.msg = msg

class ClusterState(IntEnum):
    STARTING = 0
    RUNNING = 1
    ERROR = 2
    STOPPING = 3
    STOPPED = 4

    def IsFinal(self):
        return self == ClusterState.RUNNING or self == ClusterState.ERROR \
            or self == ClusterState.STOPPED

def _WaitForFinalState(session, cluster_name=None, is_test=False):
    """
    Polls the cluster state until it hits a final state (RUNNING, STOPPED, ERROR).
    If the final state is RUNNING, also waits for the coord host to be set.
    On success, returns the cluster info returned by /rpc/GetCluster
    On error, raises Error.
    """
    while True:
        get_data = {'name':cluster_name}
        get_url = '{}/rpc/GetClusters'.format(_GetConsoleUrl(is_test))
        res = session.post(get_url, data=get_data,
                           headers={'X-CSRFToken':session.cookies['csrftoken'], 'Referer':get_url})
        if res.status_code != requests.codes.ok or len(res.json()) == 0:
            raise Error('Unknown cluster: {}'.format(cluster_name))
        cluster = res.json()[0]
        logger.debug('cluster state: {}'.format(ClusterState(cluster['state']).name))
        if cluster['state'] == ClusterState.ERROR:
            raise Error('Cluster {} has an error'.format(cluster_name))
        # if we're waiting for 'running' we also want the coord host to be set
        if ClusterState(cluster['state']).IsFinal() \
            and (cluster['state'] != ClusterState.RUNNING or cluster['coord_host'] is not None):
            return cluster
        time.sleep(10)

def _GetConsoleUrl(is_test=False):
    if is_test:
        return 'http://localhost:8000'
    else:
        return 'https://prod-console.dev.leodata.io'

def _LogIn(session, account_name, user_name, password, is_test=False):
    """
    Log in to console.
    """
    login_data = {'account_name':account_name, 'user_name':user_name, 'password':password}
    res = session.post('{}/rpc/LogIn'.format(_GetConsoleUrl(is_test)), data=login_data)
    if res.status_code != requests.codes.ok:
        raise Error('login failed')

def _StartCluster(session, cluster_id, restart_as_on_demand, is_test=False):
    start_data = { 'id':cluster_id, 'restart_as_on_demand':int(restart_as_on_demand) }
    start_url = '{}/rpc/StartCluster'.format(_GetConsoleUrl(is_test))
    res = session.post(start_url, data=start_data,
                       headers={'X-CSRFToken':session.cookies['csrftoken'], 'Referer':start_url})
    if res.status_code != requests.codes.ok:
        raise Error('Cluster start failed')

def _StopCluster(session, cluster_id, is_test=False):
    stop_data = { 'id':cluster_id }
    stop_url = '{}/rpc/StopCluster'.format(_GetConsoleUrl(is_test))
    res = session.post(stop_url, data=stop_data,
                       headers={'X-CSRFToken':session.cookies['csrftoken'], 'Referer':stop_url})
    if res.status_code != requests.codes.ok:
        raise Error('Cluster stop failed')

def Connect(account=None, user_name=None, password=None, cluster_name=None,
            restart_as_on_demand=True, is_test=False):
    assert account is not None
    assert user_name is not None
    assert password is not None
    assert cluster_name is not None

    # log in
    session = requests.Session()
    _LogIn(session, account, user_name, password, is_test)

    # figure out what's going on with the cluster
    cluster = _WaitForFinalState(session, cluster_name, is_test)

    if cluster['state'] == ClusterState.RUNNING:
        # nothing left to do
        return Connection(cluster['id'], cluster['coord_host'], user_name, password,
                          session=session, stop_on_close=False, is_test=is_test)

    assert cluster['state'] == ClusterState.STOPPED
    _StartCluster(session, cluster['id'], restart_as_on_demand, is_test)
    cluster = _WaitForFinalState(session, cluster_name, is_test)
    if cluster['state'] == ClusterState.RUNNING:
        return Connection(cluster['id'], cluster['coord_host'], user_name, password,
                          session=session, stop_on_close=True, is_test=is_test)
    # TODO: retry?
    if cluster['state'] == ClusterState.STOPPED:
        raise Error('Cluster start failed')
