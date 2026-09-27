from controller.security_controller import QSentinelController


def main():

    print("================================")
    print("        Q-SENTINEL")
    print("     Admin Recovery Test")
    print("================================")

    system = QSentinelController()

    # ==========================================
    # STEP 1 — CREATE TAMPER LOCKDOWN
    # ==========================================

    print("\n[1] Creating Tamper Lockdown")
    print("------------------------------")

    for attempt in range(1, 4):

        state = system.check_tamper(
            door_open=True,
            vibration=True
        )

        print(
            f"Tamper Event {attempt} : {state}"
        )

    print("\nSystem Status:")
    print(system.status())

    # ==========================================
    # STEP 2 — NORMAL AUTHENTICATION BLOCKED
    # ==========================================

    print("\n[2] Testing Authentication During Lockdown")
    print("--------------------------------------------")

    rfid = system.verify_rfid(
        "Q-SENTINEL-USER-01"
    )

    quantum = system.verify_quantum()

    access = system.authenticate(
        rfid_valid=rfid,
        face_valid=True,
        quantum_valid=quantum
    )

    print(
        "Normal Authentication :",
        "GRANTED 🔓" if access
        else "BLOCKED 🔒"
    )

    # ==========================================
    # STEP 3 — WRONG ADMIN CREDENTIAL
    # ==========================================

    print("\n[3] Testing Invalid Admin Credentials")
    print("--------------------------------------")

    recovery = system.admin_recovery(
        admin_id="Q-ADMIN-01",
        admin_password="WRONG-PASSWORD"
    )

    print(
        "Recovery :",
        "SUCCESS ✅" if recovery
        else "DENIED ❌"
    )

    print("\nSystem Status:")
    print(system.status())

    # ==========================================
    # STEP 4 — CORRECT ADMIN RECOVERY
    # ==========================================

    print("\n[4] Testing Valid Admin Recovery")
    print("---------------------------------")

    recovery = system.admin_recovery(
        admin_id="Q-ADMIN-01",
        admin_password="QADMIN-2026"
    )

    print(
        "Recovery :",
        "SUCCESS ✅" if recovery
        else "DENIED ❌"
    )

    # ==========================================
    # STEP 5 — FINAL SYSTEM STATUS
    # ==========================================

    print("\n[5] Final System Status")
    print("-----------------------")

    print(system.status())

    print("\n================================")
    print(" Admin Recovery Test Completed")
    print("================================")


if __name__ == "__main__":
    main()