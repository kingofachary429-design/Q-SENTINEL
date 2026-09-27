from tamper.tamper_monitor import TamperMonitor
from logs.security_logger import SecurityLogger


def main():

    print("================================")
    print("        Q-SENTINEL")
    print(" Tamper + Security Logging")
    print("================================")

    monitor = TamperMonitor(max_events=3)
    logger = SecurityLogger()

    # --------------------------------
    # TAMper EVENT 1
    # --------------------------------

    print("\n[1] Door Opening")

    state = monitor.check(
        door_open=True,
        vibration=False
    )

    print("Tamper State :", state.value)

    logger.log(
        event="TAMPER",
        rfid="N/A",
        face="N/A",
        quantum="N/A",
        security_level=state.value,
        result="WARNING"
    )

    # --------------------------------
    # TAMPER EVENT 2
    # --------------------------------

    print("\n[2] Vibration")

    state = monitor.check(
        door_open=False,
        vibration=True
    )

    print("Tamper State :", state.value)

    logger.log(
        event="TAMPER",
        rfid="N/A",
        face="N/A",
        quantum="N/A",
        security_level=state.value,
        result="WARNING"
    )

    # --------------------------------
    # TAMPER EVENT 3
    # --------------------------------

    print("\n[3] Repeated Tamper")

    state = monitor.check(
        door_open=True,
        vibration=True
    )

    print("Tamper State :", state.value)

    if monitor.is_locked():

        logger.log(
            event="TAMPER_LOCKDOWN",
            rfid="N/A",
            face="N/A",
            quantum="N/A",
            security_level=state.value,
            result="LOCKDOWN"
        )

        print("\n🔒 SYSTEM LOCKDOWN")

    print("\n================================")
    print(" Tamper Logging Completed")
    print("================================")


if __name__ == "__main__":
    main()