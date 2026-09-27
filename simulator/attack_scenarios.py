from controller.security_controller import QSentinelController


def show_status(system):

    print("System Status:")
    print(system.status())


def main():

    print("================================")
    print("        Q-SENTINEL")
    print("     Attack Scenario Test")
    print("================================")

    # --------------------------------
    # SCENARIO 1 — WRONG RFID
    # --------------------------------

    print("\n[SCENARIO 1]")
    print("Unauthorized RFID")
    print("------------------------------")

    system = QSentinelController()

    rfid = system.verify_rfid(
        "UNKNOWN-CARD-999"
    )

    print(
        "RFID :",
        "PASS ✅" if rfid else "FAIL ❌"
    )

    access = system.authenticate(
        rfid_valid=rfid,
        face_valid=False,
        quantum_valid=False
    )

    print(
        "ACCESS GRANTED 🔓"
        if access
        else "ACCESS DENIED 🔒"
    )

    show_status(system)

    # --------------------------------
    # SCENARIO 2 — WRONG FACE
    # --------------------------------

    print("\n[SCENARIO 2]")
    print("Valid RFID + Unauthorized Face")
    print("------------------------------")

    system = QSentinelController()

    rfid = system.verify_rfid(
        "Q-SENTINEL-USER-01"
    )

    access = system.authenticate(
        rfid_valid=rfid,
        face_valid=False,
        quantum_valid=False
    )

    print("RFID : PASS ✅")
    print("Face : FAIL ❌")

    print(
        "ACCESS GRANTED 🔓"
        if access
        else "ACCESS DENIED 🔒"
    )

    show_status(system)

    # --------------------------------
    # SCENARIO 3 — TAMPER ATTACK
    # --------------------------------

    print("\n[SCENARIO 3]")
    print("Physical Tamper Attack")
    print("------------------------------")

    system = QSentinelController()

    for attempt in range(1, 4):

        state = system.check_tamper(
            door_open=True,
            vibration=True
        )

        print(
            f"Tamper Event {attempt} : {state}"
        )

    print("\nFinal Tamper Status:")
    print(system.status()["tamper"])

    # --------------------------------
    # SCENARIO 4 — LOCKED SYSTEM
    # --------------------------------

    print("\n[SCENARIO 4]")
    print("Authentication After Tamper Lockdown")
    print("--------------------------------------")

    rfid = system.verify_rfid(
        "Q-SENTINEL-USER-01"
    )

    quantum = system.verify_quantum()

    access = system.authenticate(
        rfid_valid=rfid,
        face_valid=True,
        quantum_valid=quantum
    )

    print("RFID    :", "PASS ✅" if rfid else "FAIL ❌")
    print("Face    : PASS ✅")
    print("Quantum :", "PASS ✅" if quantum else "FAIL ❌")

    print(
        "\nACCESS GRANTED 🔓"
        if access
        else "\nACCESS DENIED 🔒"
    )

    show_status(system)

    print("\n================================")
    print(" Attack Testing Completed")
    print("================================")


if __name__ == "__main__":
    main()