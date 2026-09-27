from security.security_engine import SecurityEngine
from quantum.challenge import QuantumChallenge
from rfid.rfid_auth import RFIDAuthenticator
from tamper.tamper_monitor import TamperMonitor
from logs.security_logger import SecurityLogger


class QSentinelController:

    def __init__(self):

        # ==========================================
        # SECURITY ENGINE
        # ==========================================

        self.security = SecurityEngine(
            max_attempts=3
        )

        # ==========================================
        # QUANTUM SECURITY
        # ==========================================

        self.quantum = QuantumChallenge()

        # ==========================================
        # RFID AUTHENTICATION
        # ==========================================

        self.rfid = RFIDAuthenticator()

        # ==========================================
        # TAMPER MONITOR
        # ==========================================

        self.tamper = TamperMonitor(
            max_events=3
        )

        # ==========================================
        # SECURITY LOGGER
        # ==========================================

        self.logger = SecurityLogger()

        # ==========================================
        # SHARED SECRET
        # ==========================================

        self.secret = "Q_SENTINEL_SECRET"

        # ==========================================
        # ADMIN RECOVERY CREDENTIAL
        # ==========================================

        self.admin_id = "Q-ADMIN-01"
        self.admin_password = "QADMIN-2026"

    # ==================================================
    # RFID VERIFICATION
    # ==================================================

    def verify_rfid(self, uid):

        return self.rfid.authenticate(uid)

    # ==================================================
    # QUANTUM SECURITY VERIFICATION
    # ==================================================

    def verify_quantum(self):

        # Generate quantum random challenge
        challenge, quantum_bits, circuit = (
            self.quantum.generate_challenge()
        )

        # Generate response
        response = self.quantum.generate_response(
            challenge,
            self.secret
        )

        # Verify response
        verified = self.quantum.verify_response(
            challenge,
            self.secret,
            response
        )

        # ==========================================
        # DISPLAY QUANTUM INFORMATION
        # ==========================================

        print("\n================================")
        print("       QUANTUM SECURITY")
        print("================================")

        print(
            "\nQuantum Backend : "
            "Qiskit Aer Simulator"
        )

        print("\nQuantum Circuit:")
        print("------------------------------")

        print(
            circuit.draw()
        )

        print("\nQuantum Random Bits:")
        print("------------------------------")

        print(quantum_bits)

        print("\nQuantum Bits Length:")
        print("------------------------------")

        print(len(quantum_bits))

        print("\nDynamic Quantum Challenge:")
        print("------------------------------")

        print(challenge)

        print("\nQuantum Verification :",
              "PASSED ✅" if verified
              else "FAILED ❌")

        return verified

    # ==================================================
    # NORMAL AUTHENTICATION
    # ==================================================

    def authenticate(
        self,
        rfid_valid,
        face_valid,
        quantum_valid
    ):

        # ==========================================
        # TAMPER LOCKDOWN OVERRIDE
        # ==========================================

        if self.tamper.is_locked():

            self.logger.log(
                "SECURITY_LOCKDOWN",
                "BLOCKED",
                "BLOCKED",
                "BLOCKED",
                "LOCKDOWN",
                "DENIED"
            )

            return False

        # ==========================================
        # RFID CHECK
        # ==========================================

        if not rfid_valid:

            self.security.authenticate(
                False,
                False
            )

            self.logger.log(
                "AUTHENTICATION",
                "FAIL",
                "N/A",
                "N/A",
                self.security.level.value,
                "DENIED"
            )

            return False

        # ==========================================
        # FACE CHECK
        # ==========================================

        if not face_valid:

            self.security.authenticate(
                True,
                False
            )

            self.logger.log(
                "AUTHENTICATION",
                "PASS",
                "FAIL",
                "N/A",
                self.security.level.value,
                "DENIED"
            )

            return False

        # ==========================================
        # QUANTUM CHECK
        # ==========================================

        if not quantum_valid:

            self.security.authenticate(
                True,
                False
            )

            self.logger.log(
                "AUTHENTICATION",
                "PASS",
                "PASS",
                "FAIL",
                self.security.level.value,
                "DENIED"
            )

            return False

        # ==========================================
        # FINAL SECURITY ENGINE CHECK
        # ==========================================

        result = self.security.authenticate(
            True,
            True
        )

        # ==========================================
        # LOG FINAL RESULT
        # ==========================================

        self.logger.log(
            "AUTHENTICATION",
            "PASS",
            "PASS",
            "PASS",
            self.security.level.value,
            "GRANTED"
            if result
            else "DENIED"
        )

        return result

    # ==================================================
    # TAMPER MONITORING
    # ==================================================

    def check_tamper(
        self,
        door_open=False,
        vibration=False
    ):

        state = self.tamper.check(
            door_open,
            vibration
        )

        # ==========================================
        # TAMPER LOCKDOWN
        # ==========================================

        if self.tamper.is_locked():

            self.logger.log(
                "TAMPER_LOCKDOWN",
                "N/A",
                "N/A",
                "N/A",
                "LOCKDOWN",
                "LOCKDOWN"
            )

        # ==========================================
        # TAMPER WARNING
        # ==========================================

        elif state.value == "WARNING":

            self.logger.log(
                "TAMPER",
                "N/A",
                "N/A",
                "N/A",
                "WARNING",
                "WARNING"
            )

        return state.value

    # ==================================================
    # ADMIN AUTHENTICATION
    # ==================================================

    def authenticate_admin(
        self,
        admin_id,
        admin_password
    ):

        # ==========================================
        # VERIFY ADMIN CREDENTIALS
        # ==========================================

        if (
            admin_id == self.admin_id
            and
            admin_password == self.admin_password
        ):

            self.logger.log(
                "ADMIN_AUTHENTICATION",
                "PASS",
                "PASS",
                "PASS",
                "LOCKDOWN"
                if self.tamper.is_locked()
                else self.security.level.value,
                "GRANTED"
            )

            return True

        # ==========================================
        # ADMIN AUTHENTICATION FAILED
        # ==========================================

        self.logger.log(
            "ADMIN_AUTHENTICATION",
            "FAIL",
            "FAIL",
            "FAIL",
            "LOCKDOWN"
            if self.tamper.is_locked()
            else self.security.level.value,
            "DENIED"
        )

        return False

    # ==================================================
    # SECURE ADMIN RECOVERY
    # ==================================================

    def admin_recovery(
        self,
        admin_id,
        admin_password
    ):

        # ==========================================
        # ADMIN AUTHENTICATION
        # ==========================================

        admin_valid = self.authenticate_admin(
            admin_id,
            admin_password
        )

        if not admin_valid:

            print(
                "❌ Admin authentication failed."
            )

            return False

        # ==========================================
        # CHECK LOCKDOWN
        # ==========================================

        if not self.tamper.is_locked():

            print(
                "ℹ️ System is not in tamper lockdown."
            )

            return False

        # ==========================================
        # ADMIN RECOVERY AUTHORIZED
        # ==========================================

        print(
            "\n🔐 ADMIN RECOVERY AUTHORIZED"
        )

        # Reset tamper state
        self.tamper.reset()

        # Reset security engine
        self.security.reset()

        # ==========================================
        # LOG RECOVERY
        # ==========================================

        self.logger.log(
            "ADMIN_RECOVERY",
            "PASS",
            "PASS",
            "PASS",
            "NORMAL",
            "RECOVERED"
        )

        print(
            "✅ Tamper lockdown cleared."
        )

        print(
            "✅ Security engine reset."
        )

        print(
            "✅ System restored to NORMAL."
        )

        return True

    # ==================================================
    # SYSTEM STATUS
    # ==================================================

    def status(self):

        security_status = (
            self.security.status()
        )

        tamper_status = (
            self.tamper.status()
        )

        # ==========================================
        # DETERMINE OVERALL STATE
        # ==========================================

        if tamper_status["locked"]:

            overall_state = "LOCKDOWN"

        elif security_status["locked"]:

            overall_state = "LOCKDOWN"

        elif (
            tamper_status["state"] == "WARNING"
            or
            security_status["security_level"] == "HIGH"
        ):

            overall_state = "HIGH"

        else:

            overall_state = "NORMAL"

        return {
            "overall_state": overall_state,
            "security": security_status,
            "tamper": tamper_status
        }

    # ==================================================
    # FULL SYSTEM RESET
    # ==================================================

    def reset_system(self):

        self.security.reset()

        self.tamper.reset()

        self.logger.log(
            "SYSTEM_RESET",
            "N/A",
            "N/A",
            "N/A",
            "NORMAL",
            "RESET"
        )

        return self.status()