from security.security_engine import SecurityEngine


def print_status(engine):
    status = engine.status()

    print("Security Level :", status["security_level"])
    print("Failed Attempts:", status["failed_attempts"])
    print("Locked          :", status["locked"])


def main():

    print("================================")
    print("      Q-SENTINEL")
    print("   Security Attack Simulator")
    print("================================")

    engine = SecurityEngine(max_attempts=3)

    # --------------------------------
    # TEST 1 — VALID AUTHENTICATION
    # --------------------------------

    print("\n[TEST 1] Valid Authentication")
    print("------------------------------")

    result = engine.authenticate(
        rfid_valid=True,
        face_valid=True
    )

    print(
        "ACCESS GRANTED 🔓"
        if result
        else "ACCESS DENIED 🔒"
    )

    print_status(engine)

    # --------------------------------
    # RESET
    # --------------------------------

    engine.reset()

    # --------------------------------
    # TEST 2 — WRONG FACE
    # --------------------------------

    print("\n[TEST 2] Wrong Face")
    print("------------------------------")

    result = engine.authenticate(
        rfid_valid=True,
        face_valid=False
    )

    print(
        "ACCESS GRANTED 🔓"
        if result
        else "ACCESS DENIED 🔒"
    )

    print_status(engine)

    # --------------------------------
    # TEST 3 — REPEATED ATTACK
    # --------------------------------

    print("\n[TEST 3] Repeated Authentication Attack")
    print("----------------------------------------")

    engine.reset()

    for attempt in range(1, 5):

        result = engine.authenticate(
            rfid_valid=False,
            face_valid=False
        )

        print(f"\nAttempt {attempt}")

        print(
            "ACCESS GRANTED 🔓"
            if result
            else "ACCESS DENIED 🔒"
        )

        print_status(engine)

    # --------------------------------
    # TEST 4 — LOCKDOWN TEST
    # --------------------------------

    print("\n[TEST 4] Lockdown Verification")
    print("------------------------------")

    result = engine.authenticate(
        rfid_valid=True,
        face_valid=True
    )

    print(
        "ACCESS GRANTED 🔓"
        if result
        else "ACCESS DENIED 🔒"
    )

    print_status(engine)

    print("\n================================")
    print(" Security Testing Completed")
    print("================================")


if __name__ == "__main__":
    main()