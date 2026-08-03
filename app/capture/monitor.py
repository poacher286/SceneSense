from mss import mss


class MonitorManager:

    def __init__(self):

        self.sct = mss()

    def get_primary_monitor(self):

        # monitors[0] = virtual monitor
        # monitors[1] = first physical monitor

        return self.sct.monitors[1]

    def list_monitors(self):

        return self.sct.monitors