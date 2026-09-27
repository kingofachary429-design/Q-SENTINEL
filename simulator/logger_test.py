from logs.security_logger import SecurityLogger


def main():

    logger = SecurityLogger()

    logger.log(
        event="AUTHENTICATION",
        rfid="PASS",
        face="PASS",
        quantum="PASS",
        security_level="NORMAL",
        result="GRANTED"
    )

    logger.log(
        event="AUTHENTICATION",
        rfid="PASS",
        face="FAIL",
        quantum="N/A",
        security_level="HIGH",
        result="DENIED"
    )

    logger.log(
        event="ATTACK",
        rfid="FAIL",
        face="FAIL",
        quantum="N/A",
        security_level="LOCKDOWN",
        result="DENIED"
    )

    print("\nLogging test completed.")


if __name__ == "__main__":
    main()