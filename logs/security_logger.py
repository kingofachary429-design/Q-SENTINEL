from datetime import datetime
import os


LOG_FILE = os.path.join(
    "logs",
    "security_events.log"
)


class SecurityLogger:

    def __init__(self):
        os.makedirs("logs", exist_ok=True)

    def log(
        self,
        event,
        rfid,
        face,
        quantum,
        security_level,
        result
    ):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        log_entry = (
            f"{timestamp} | "
            f"EVENT={event} | "
            f"RFID={rfid} | "
            f"FACE={face} | "
            f"QUANTUM={quantum} | "
            f"LEVEL={security_level} | "
            f"RESULT={result}\n"
        )

        with open(
            LOG_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(log_entry)

        print("📝 Security event logged.")