from tamper.tamper_monitor import TamperMonitor


def main():

    print("================================")
    print("        Q-SENTINEL")
    print("    Tamper Detection Test")
    print("================================")

    monitor = TamperMonitor(max_events=3)

    # --------------------------------
    # NORMAL STATE
    # --------------------------------

    print("\n[TEST 1] Normal Environment")
    print("------------------------------")

    state = monitor.check(
        door_open=False,
        vibration=False
    )

    print("Tamper State :", state.value)
    print("Status       :", monitor.status())

    # --------------------------------
    # DOOR OPEN
    # --------------------------------

    print("\n[TEST 2] Unauthorized Door Opening")
    print("------------------------------------")

    state = monitor.check(
        door_open=True,
        vibration=False
    )

    print("🚨 DOOR OPEN DETECTED")
    print("Tamper State :", state.value)
    print("Status       :", monitor.status())

    # --------------------------------
    # VIBRATION
    # --------------------------------

    print("\n[TEST 3] Vibration Detection")
    print("------------------------------")

    state = monitor.check(
        door_open=False,
        vibration=True
    )

    print("🚨 VIBRATION DETECTED")
    print("Tamper State :", state.value)
    print("Status       :", monitor.status())

    # --------------------------------
    # THIRD ATTACK
    # --------------------------------

    print("\n[TEST 4] Repeated Tamper Attack")
    print("-------------------------------")

    state = monitor.check(
        door_open=True,
        vibration=True
    )

    print("🚨 MULTIPLE TAMPER SIGNALS")
    print("Tamper State :", state.value)
    print("Status       :", monitor.status())

    # --------------------------------
    # LOCKDOWN CHECK
    # --------------------------------

    print("\n[TEST 5] Lockdown Verification")
    print("------------------------------")

    print(
        "🔒 SYSTEM LOCKED"
        if monitor.is_locked()
        else "System still active"
    )

    print("\n================================")
    print(" Tamper Testing Completed")
    print("================================")


if __name__ == "__main__":
    main()