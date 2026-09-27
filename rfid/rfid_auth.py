class RFIDAuthenticator:

    def __init__(self):
        # Temporary authorized UID
        # Later this will come from the real RC522 reader
        self.authorized_uids = {
            "Q-SENTINEL-USER-01"
        }

    def authenticate(self, uid):
        """
        Verify whether the scanned RFID UID
        belongs to an authorized user.
        """

        if uid in self.authorized_uids:
            return True

        return False

    def add_authorized_uid(self, uid):
        self.authorized_uids.add(uid)

    def remove_authorized_uid(self, uid):
        self.authorized_uids.discard(uid)

    def get_authorized_uids(self):
        return list(self.authorized_uids)