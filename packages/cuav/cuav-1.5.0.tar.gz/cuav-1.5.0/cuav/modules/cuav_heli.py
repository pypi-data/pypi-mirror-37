"""
cuav helicopter monitoring module for MAVProxy
"""

import os, sys, math, time

from pymavlink import mavutil
from MAVProxy.modules.lib import mp_util
from MAVProxy.modules.lib import mp_module

class CUAVHeliModule(mp_module.MPModule):
    def __init__(self, mpstate):
        super(CUAVHeliModule, self).__init__(mpstate, "cuav_heli", "CUAV Heli", public=False)
        self.console.set_status('IGN', 'IGN', row=4)
        self.console.set_status('THR', 'THR', row=4)
        self.console.set_status('RPM', 'RPM: 0', row=4)

    def mavlink_packet(self, msg):
        '''handle an incoming mavlink packet'''
        type = msg.get_type()

        master = self.master

        # add some status fields
        if type in [ 'RC_CHANNELS_RAW' ]:
            rc6 = msg.chan6_raw
            if rc6 > 1500:
                ign_colour = 'green'
            else:
                ign_colour = 'red'
            self.console.set_status('IGN', 'IGN', fg=ign_colour)

        if type in [ 'SERVO_OUTPUT_RAW' ]:
            rc8 = msg.servo8_raw
            if rc8 < 1200:
                thr_colour = 'red'
            elif rc8 < 1300:
                thr_colour = 'orange'
            else:
                thr_colour = 'green'
            self.console.set_status('THR', 'THR', fg=thr_colour)

        if type in [ 'RPM' ]:
            rpm = msg.rpm1
            if rpm < 3000:
                rpm_colour = 'red'
            elif rpm < 10000:
                rpm_colour = 'orange'
            else:
                rpm_colour = 'green'
            self.console.set_status('RPM', 'RPM: %u' % rpm, fg=rpm_colour)

def init(mpstate):
    '''initialise module'''
    return CUAVHeliModule(mpstate)
