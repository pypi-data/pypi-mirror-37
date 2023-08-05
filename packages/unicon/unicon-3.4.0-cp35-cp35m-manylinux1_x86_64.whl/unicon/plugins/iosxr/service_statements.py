
from unicon.eal.dialogs import Statement

from .service_patterns import IOSXRSwitchoverPatterns

pat = IOSXRSwitchoverPatterns()

prompt_switchover_stmt = Statement(pattern=pat.prompt_switchover,
                              action='sendline()',
                              args=None,
                              loop_continue=True,
                              continue_timer=True)

rp_in_standby_stmt = Statement(pattern=pat.rp_in_standby,
                               action=None,
                               args=None,
                               loop_continue=False,
                               continue_timer=False)

switchover_statement_list = [prompt_switchover_stmt,
                             rp_in_standby_stmt # loop_continue = False
                             ]

