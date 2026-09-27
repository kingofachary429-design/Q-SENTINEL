from enum import Enum


class TamperState(Enum):
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    LOCKDOWN = "LOCKDOWN"


class TamperMonitor:

    def __init__(self, max_events=3):
        self.tamper_events = 0
        self.max_events = max_events
        self.state = TamperState.NORMAL

    def check(self, door_open=False, vibration=False):

        # No tamper detected
        if not door_open and not vibration:
            return self.state

        # Tamper detected
        self.tamper_events += 1

        if self.tamper_events >= self.max_events:
            self.state = TamperState.LOCKDOWN

        else:
            self.state = TamperState.WARNING

        return self.state

    def is_locked(self):
        return self.state == TamperState.LOCKDOWN

    def reset(self):
        self.tamper_events = 0
        self.state = TamperState.NORMAL

    def status(self):

        return {
            "tamper_events": self.tamper_events,
            "state": self.state.value,
            "locked": self.is_locked()
        }