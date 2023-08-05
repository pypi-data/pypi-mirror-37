# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Tooz Coordination and locking utilities."""

import inspect
import itertools
import random

import decorator
import eventlet
from oslo_config import cfg
from oslo_log import log
from oslo_service import loopingcall
from oslo_utils import uuidutils
import six
from tooz import coordination
from tooz import locking

from manila import exception
from manila.i18n import _, _LE, _LI, _LW


LOG = log.getLogger(__name__)


coordination_opts = [
    cfg.StrOpt('backend_url',
               default='file://$state_path',
               help='The back end URL to use for distributed coordination.'),
    cfg.FloatOpt('heartbeat',
                 default=1.0,
                 help='Number of seconds between heartbeats for distributed '
                      'coordination.'),
    cfg.FloatOpt('initial_reconnect_backoff',
                 default=0.1,
                 help='Initial number of seconds to wait after failed '
                      'reconnection.'),
    cfg.FloatOpt('max_reconnect_backoff',
                 default=60.0,
                 help='Maximum number of seconds between sequential '
                      'reconnection retries.'),
]

CONF = cfg.CONF
CONF.register_opts(coordination_opts, group='coordination')


class Coordinator(object):
    """Tooz coordination wrapper.

    Coordination member id is created from concatenated `prefix` and
    `agent_id` parameters.

    :param str agent_id: Agent identifier
    :param str prefix: Used to provide member identifier with a
    meaningful prefix.
    """

    def __init__(self, agent_id=None, prefix=''):
        self.coordinator = None
        self.agent_id = agent_id or uuidutils.generate_uuid()
        self.started = False
        self.prefix = prefix
        self._heartbeat_thread = loopingcall.FixedIntervalLoopingCall(
            self.heartbeat)

    def _is_active(self):
        return self.started

    def start(self):
        """Connect to coordination back end and start heartbeat."""
        if not self._is_active():
            try:
                self._start()
                self.started = True
                # NOTE(gouthamr): Start heartbeat in separate thread to avoid
                # being blocked by long co-routines.
                if self.coordinator and self.coordinator.requires_beating:
                    LOG.debug("This tooz lock management back end supports "
                              "heart beats. Spawning a new thread to "
                              "send regular heart beats.")
                    self._heartbeat_thread.start(
                        cfg.CONF.coordination.heartbeat)
                else:
                    LOG.debug("This tooz lock management back end does not "
                              "support heart beats.")
            except coordination.ToozError:
                LOG.exception(_LE('Error starting coordination back end.'))
                raise
            LOG.info(_LI('Coordination back end started successfully.'))

    def stop(self):
        """Disconnect from coordination back end and stop heartbeat."""
        msg = _('Stopped Coordinator (Agent ID: %(agent)s, prefix: '
                '%(prefix)s)')
        msg_args = {'agent': self.agent_id, 'prefix': self.prefix}
        if self._is_active():

            debug_msg = ('Stopping heartbeat thread for coordinator with '
                         '(Agent ID: %(agent)s, prefix: %(prefix)s).')
            LOG.debug(debug_msg, msg_args)
            if self._heartbeat_thread is not None:
                self._heartbeat_thread.stop()
                self._heartbeat_thread = None
            self.coordinator.stop()
            self.coordinator = None
            self.started = False

        LOG.info(msg, msg_args)

    def get_lock(self, name):
        """Return a Tooz back end lock.

        :param str name: The lock name that is used to identify it
            across all nodes.
        """
        # NOTE(gouthamr): Tooz expects lock name as a byte string
        lock_name = (self.prefix + name).encode('ascii')
        if self._is_active():
            return self.coordinator.get_lock(lock_name)
        else:
            raise exception.LockCreationFailed(_('Coordinator uninitialized.'))

    def heartbeat(self):
        """Coordinator heartbeat.

        Method that every couple of seconds (config: `coordination.heartbeat`)
        sends heartbeat to prove that the member is not dead.

        If connection to coordination back end is broken it tries to
        reconnect every couple of seconds
        (config: `coordination.initial_reconnect_backoff` up to
        `coordination.max_reconnect_backoff`)

        """
        if self._is_active():
            try:
                self._heartbeat()
            except coordination.ToozConnectionError:
                self._reconnect()

    def _start(self):
        # NOTE(gouthamr): Tooz expects member_id as a byte string.
        member_id = (self.prefix + self.agent_id).encode('ascii')
        self.coordinator = coordination.get_coordinator(
            cfg.CONF.coordination.backend_url, member_id)
        self.coordinator.start()

    def _heartbeat(self):
        try:
            self.coordinator.heartbeat()
        except coordination.ToozConnectionError:
            LOG.exception(_LE('Connection error while sending a heartbeat '
                              'to coordination back end.'))
            raise
        except coordination.ToozError:
            LOG.exception(_LE('Error sending a heartbeat to coordination '
                              'back end.'))

    def _reconnect(self):
        """Reconnect with jittered exponential back off."""
        LOG.info(_LI('Reconnecting to coordination back end.'))
        cap = cfg.CONF.coordination.max_reconnect_backoff
        backoff = base = cfg.CONF.coordination.initial_reconnect_backoff
        for attempt in itertools.count(1):
            try:
                self._start()
                break
            except coordination.ToozError:
                backoff = min(cap, random.uniform(base, backoff * 3))
                msg = _LW('Reconnect attempt %(attempt)s failed. '
                          'Next try in %(backoff).2fs.')
                LOG.warning(msg, {'attempt': attempt, 'backoff': backoff})
                eventlet.sleep(backoff)
        LOG.info(_LI('Reconnected to coordination back end.'))


LOCK_COORDINATOR = Coordinator(prefix='manila-')


class Lock(locking.Lock):
    """Lock with dynamic name.

    :param str lock_name: Lock name.
    :param dict lock_data: Data for lock name formatting.
    :param coordinator: Coordinator object to use when creating lock.
        Defaults to the global coordinator.

    Using it like so::

        with Lock('mylock'):
           ...

    ensures that only one process at a time will execute code in context.
    Lock name can be formatted using Python format string syntax::

        Lock('foo-{share.id}, {'share': ...,}')

    Available field names are keys of lock_data.
    """
    def __init__(self, lock_name, lock_data=None, coordinator=None):
        super(Lock, self).__init__(six.text_type(id(self)))
        lock_data = lock_data or {}
        self.coordinator = coordinator or LOCK_COORDINATOR
        self.blocking = True
        self.lock = self._prepare_lock(lock_name, lock_data)

    def _prepare_lock(self, lock_name, lock_data):
        if not isinstance(lock_name, six.string_types):
            raise ValueError(_('Not a valid string: %s') % lock_name)
        return self.coordinator.get_lock(lock_name.format(**lock_data))

    def acquire(self, blocking=None):
        """Attempts to acquire lock.

        :param blocking: If True, blocks until the lock is acquired. If False,
            returns right away. Otherwise, the value is used as a timeout
            value and the call returns maximum after this number of seconds.
        :return: returns true if acquired (false if not)
        :rtype: bool
        """
        blocking = self.blocking if blocking is None else blocking
        return self.lock.acquire(blocking=blocking)

    def release(self):
        """Attempts to release lock.

        The behavior of releasing a lock which was not acquired in the first
        place is undefined.
        """
        self.lock.release()


def synchronized(lock_name, blocking=True, coordinator=None):
    """Synchronization decorator.

    :param str lock_name: Lock name.
    :param blocking: If True, blocks until the lock is acquired.
            If False, raises exception when not acquired. Otherwise,
            the value is used as a timeout value and if lock is not acquired
            after this number of seconds exception is raised.
    :param coordinator: Coordinator object to use when creating lock.
        Defaults to the global coordinator.
    :raises tooz.coordination.LockAcquireFailed: if lock is not acquired

    Decorating a method like so::

        @synchronized('mylock')
        def foo(self, *args):
           ...

    ensures that only one process will execute the foo method at a time.

    Different methods can share the same lock::

        @synchronized('mylock')
        def foo(self, *args):
           ...

        @synchronized('mylock')
        def bar(self, *args):
           ...

    This way only one of either foo or bar can be executing at a time.

    Lock name can be formatted using Python format string syntax::

        @synchronized('{f_name}-{shr.id}-{snap[name]}')
        def foo(self, shr, snap):
           ...

    Available field names are: decorated function parameters and
    `f_name` as a decorated function name.
    """
    @decorator.decorator
    def _synchronized(f, *a, **k):
        call_args = inspect.getcallargs(f, *a, **k)
        call_args['f_name'] = f.__name__
        lock = Lock(lock_name, call_args, coordinator)
        with lock(blocking):
            LOG.debug('Lock "%(name)s" acquired by "%(function)s".',
                      {'name': lock_name, 'function': f.__name__})
            return f(*a, **k)
    return _synchronized
