__copyright__ = "# Copyright (c) 2016 by cisco Systems, Inc. All rights reserved."
__author__ = "Syed Raza <syedraza@cisco.com>"

import re
from time import sleep
from datetime import datetime, timedelta

from unicon.plugins.generic import service_implementation as svc
from unicon.bases.routers.services import BaseService
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog

from .service_statements import switchover_statement_list

class Configure(svc.Configure):
    def __init__(self, connection, context, **kwargs):
        super().__init__(connection, context, **kwargs)
        self.start_state = 'config'
        self.end_state = 'enable'
        self.service_name = 'config'


class AdminExecute(svc.Execute):
    def __init__(self, connection, context, **kwargs):
        super().__init__(connection, context, **kwargs)
        self.start_state = 'admin'
        self.end_state = 'enable'
        self.service_name = 'admin'


class AdminConfigure(svc.Configure):
    def __init__(self, connection, context, **kwargs):
        super().__init__(connection, context, **kwargs)
        self.start_state = 'admin_conf'
        self.end_state = 'enable'
        self.service_name = 'admin_conf'


class HAExecute(svc.HaExecService):
    def __init__(self, connection, context, **kwargs):
        super().__init__(connection, context, **kwargs)
        self.start_state = 'enable'
        self.end_state = 'enable'
        self.service_name = 'execute'


class Switchover(BaseService):
    """ Service to switchover the device.

    Arguments:
        command: command to do switchover. default
                 "redundancy switchover"
        dialog: Dialog which include list of Statements for
                additional dialogs prompted by switchover command,
                in-case it is not in the current list.
        timeout: Timeout value in sec, Default Value is 500 sec

    Returns:
        True on Success, raise SubCommandFailure on failure.

    Example:
        .. code-block:: python

            rtr.switchover()
            # If switchover command is other than 'redundancy switchover'
            rtr.switchover(command="command which invoke switchover",
            timeout=700)
    """

    def __init__(self, connection, context, **kwargs):
        super().__init__(connection, context, **kwargs)
        self.start_state = 'enable'
        self.end_state = 'enable'
        self.service_name = 'switchover'
        self.timeout = connection.settings.SWITCHOVER_TIMEOUT
        self.dialog = Dialog(switchover_statement_list)

    def call_service(self, command='redundancy switchover',
                     dialog=Dialog([]),
                     timeout=None,
                     sync_standby=True,
                     error_pattern=None,
                     *args,
                     **kwargs):
        # create an alias for connection.
        con = self.connection

        if error_pattern is None:
            self.error_pattern = con.settings.ERROR_PATTERN
        else:
            self.error_pattern = error_pattern

        start_time = datetime.now()
        timeout = timeout or self.timeout

        con.log.debug("+++ Issuing switchover on  %s  with "
                      "switchover_command %s and timeout is %s +++"
                      % (con.hostname, command, timeout))

        dialog += self.dialog

        # Issue switchover command
        con.active.spawn.sendline(command)
        try:
            self.result = dialog.process(con.active.spawn,
                           timeout=self.timeout,
                           prompt_recovery=self.prompt_recovery,
                           context=con.context)
        except SubCommandFailure as err:
            raise SubCommandFailure("Switchover Failed %s" % str(err))

        output = ""
        if self.result:
            self.result = self.get_service_result()
            output += self.result.match_output

        con.log.info('Switchover done, switching sessions')
        con.active.spawn.sendline()
        con.standby.spawn.sendline()
        con.connection_provider.prompt_recovery = True
        con.connection_provider.connect()
        con.connection_provider.prompt_recovery = False

        if sync_standby:
            con.log.info('Waiting for standby state')

            delta_time = timedelta(seconds=timeout)
            current_time = datetime.now()
            while (current_time - start_time) < delta_time:
                show_redundancy = con.execute('show redundancy', prompt_recovery=True)
                standby_state = re.findall(con.settings.STANDBY_STATE_REGEX, show_redundancy)
                standby_state = [s.strip() for s in standby_state]
                con.log.info('Standy state: %s' % standby_state)
                if standby_state == con.settings.STANDBY_EXPECTED_STATE:
                    break
                wait_time = con.settings.STANDBY_STATE_INTERVAL
                con.log.info('Waiting %s seconds' % wait_time)
                sleep(wait_time)
                current_time = datetime.now()

            if current_time - start_time > delta_time:
                raise SubCommandFailure('Switchover timed out, standby state: %s' % standby_state)

        # TODO: return all/most console output, not only from the switchover
        # This requires work on the bases.router.connection_provider BaseDualRpConnectionProvider implementation
        self.result = output

