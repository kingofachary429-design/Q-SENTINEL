from controller.security_controller import QSentinelController
from face_verification.face_auth import verify_face


def main():

    print("================================")
    print("        Q-SENTINEL")
    print(" Full Quantum Security Test")
    print("================================")

    system = QSentinelController()

    # ==========================================
    # STEP 1 — RFID AUTHENTICATION
    # ==========================================

    print("\n[1] RFID AUTHENTICATION")
    print("------------------------------")

    rfid = system.verify_rfid(
        "Q-SENTINEL-USER-01"
    )

    print(
        "RFID :",
        "PASS ✅" if rfid else "FAIL ❌"
    )

    if not rfid:

        print("\n🔒 ACCESS DENIED")

        return

    # ==========================================
    # STEP 2 — FACE AUTHENTICATION
    # ==========================================

    print("\n[2] FACE AUTHENTICATION")
    print("------------------------------")

    face = verify_face()

    print(
        "Face :",
        "PASS ✅" if face else "FAIL ❌"
    )

    if not face:

        system.authenticate(
            rfid_valid=True,
            face_valid=False,
            quantum_valid=False
        )

        print("\n🔒 ACCESS DENIED")

        return

    # ==========================================
    # STEP 3 — QUANTUM SECURITY
    # ==========================================

    print("\n[3] QUANTUM SECURITY")

    quantum = system.verify_quantum()

    if not quantum:

        print("\n🔒 QUANTUM VERIFICATION FAILED")

        system.authenticate(
            rfid_valid=True,
            face_valid=True,
            quantum_valid=False
        )

        print("\n🔒 ACCESS DENIED")

        return

    # ==========================================
    # STEP 4 — FINAL SECURITY DECISION
    # ==========================================

    print("\n[4] FINAL SECURITY DECISION")
    print("------------------------------")

    access = system.authenticate(
        rfid_valid=rfid,
        face_valid=face,
        quantum_valid=quantum
    )

    if access:

        print("\n================================")
        print("       ACCESS GRANTED 🔓")
        print("================================")

    else:

        print("\n================================")
        print("       ACCESS DENIED 🔒")
        print("================================")

    # ==========================================
    # STEP 5 — TAMPER STATUS
    # ==========================================

    print("\n[5] TAMPER MONITOR")
    print("------------------------------")

    state = system.check_tamper(
        door_open=False,
        vibration=False
    )

    print(
        "Tamper State :",
        state
    )

    # ==========================================
    # STEP 6 — FINAL SYSTEM STATUS
    # ==========================================

    print("\n[6] FINAL SYSTEM STATUS")
    print("------------------------------")

    print(system.status())

    # ==========================================
    # COMPLETION
    # ==========================================

    print("\n================================")
    print(" Full Quantum Security Test")
    print(" Completed Successfully")
    print("================================")


if __name__ == "__main__":
    main()