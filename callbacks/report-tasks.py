from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    name: report-tasks
    short_description: report-tasks completed, skipped and failed after each task
    version_added: none
    description:
        - This is the non-output callback plugin which tells you how
          many tasks have been completed so far.
'''

from ansible.plugins.callback import CallbackBase
from ansible import constants as C

class CallbackModule(CallbackBase):
    '''
    This is the default callback interface, which simply prints messages
    to stdout when new callback events are received.
    '''

    CALLBACK_VERSION = 2.0
    CALLBACK_NAME = 'report-tasks'
    CALLBACK_NEEDS_ENABLED = False

    counted = int(0)
    skipped = int(0)
    failed = int(0)

    def output(self, counted, skipped, failed):
        msgfmt = 'So far: Completed %s | Skipped %s | Failed %s | Total %s'
        print(msgfmt % (counted, skipped, failed, counted + skipped + failed))

    def v2_runner_on_failed(self, result, ignore_errors=False):
        CallbackModule.failed = CallbackModule.failed + 1
        CallbackModule.output(self, CallbackModule.counted, CallbackModule.skipped, CallbackModule.failed)

    def v2_runner_on_ok(self, result):
        CallbackModule.counted = CallbackModule.counted + 1
        CallbackModule.output(self, CallbackModule.counted, CallbackModule.skipped, CallbackModule.failed)

    def v2_runner_on_skipped(self, result):
        CallbackModule.skipped = CallbackModule.skipped + 1
        CallbackModule.output(self, CallbackModule.counted, CallbackModule.skipped, CallbackModule.failed)
