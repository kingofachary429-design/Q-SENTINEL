from enum import Enum


class SecurityLevel(Enum):
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    LOCKDOWN = "LOCKDOWN"


class SecurityEngine:
    def __init__(self, max_attempts=3):
        self.failed_attempts = 0
        self.max_attempts = max_attempts
        self.level = SecurityLevel.NORMAL
        self.locked = False

    def authenticate(self, rfid_valid, face_valid):
        # Already locked
        if self.locked:
            return False

        # Both authentication factors successful
        if rfid_valid and face_valid:
            self.failed_attempts = 0
            self.level = SecurityLevel.NORMAL
            return True

        # Authentication failed
        self.failed_attempts += 1

        if self.failed_attempts >= self.max_attempts:
            self.level = SecurityLevel.LOCKDOWN
            self.locked = True
        else:
            self.level = SecurityLevel.HIGH

        return False

    def status(self):
        return {
            "security_level": self.level.value,
            "failed_attempts": self.failed_attempts,
            "locked": self.locked,
        }

    def reset(self):
        self.failed_attempts = 0
        self.level = SecurityLevel.NORMAL
        self.locked = False