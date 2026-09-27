from security.security_engine import SecurityEngine
from quantum.challenge import QuantumChallenge
from rfid.rfid_auth import RFIDAuthenticator
from face_verification.face_auth import verify_face
from logs.security_logger import SecurityLogger


def main():

    print("================================")
    print("        Q-SENTINEL")
    print(" Quantum-Adaptive Security")
    print("================================")

    engine = SecurityEngine(max_attempts=3)
    quantum = QuantumChallenge()
    rfid = RFIDAuthenticator()
    logger = SecurityLogger()

    secret = "Q_SENTINEL_SECRET"

    # --------------------------------
    # STEP 1 — RFID
    # --------------------------------

    print("\n[1] RFID Authentication")
    print("------------------------------")

    scanned_uid = "Q-SENTINEL-USER-01"

    rfid_valid = rfid.authenticate(scanned_uid)

    print("RFID UID :", scanned_uid)

    print(
        "RFID :",
        "VERIFIED ✅" if rfid_valid else "FAILED ❌"
    )

    if not rfid_valid:

        engine.authenticate(
            rfid_valid=False,
            face_valid=False
        )

        logger.log(
            event="AUTHENTICATION",
            rfid="FAIL",
            face="N/A",
            quantum="N/A",
            security_level=engine.level.value,
            result="DENIED"
        )

        print("\n🔒 ACCESS DENIED")
        print("Security Level :", engine.level.value)
        return

    # --------------------------------
    # STEP 2 — FACE
    # --------------------------------

    print("\n[2] Face Authentication")
    print("------------------------------")

    face_valid = verify_face()

    if not face_valid:

        engine.authenticate(
            rfid_valid=True,
            face_valid=False
        )

        logger.log(
            event="AUTHENTICATION",
            rfid="PASS",
            face="FAIL",
            quantum="N/A",
            security_level=engine.level.value,
            result="DENIED"
        )

        print("\n🔒 ACCESS DENIED")
        print("Security Level :", engine.level.value)
        return

    print("\nFace : VERIFIED ✅")

    # --------------------------------
    # STEP 3 — QUANTUM CHALLENGE
    # --------------------------------

    print("\n[3] Quantum Challenge")
    print("------------------------------")

    challenge = quantum.generate_challenge()

    print("Challenge:", challenge)

    response = quantum.generate_response(
        challenge,
        secret
    )

    verified = quantum.verify_response(
        challenge,
        secret,
        response
    )

    print(
        "Challenge Verification :",
        "PASSED ✅" if verified else "FAILED ❌"
    )

    # --------------------------------
    # STEP 4 — FINAL DECISION
    # --------------------------------

    if verified:

        result = engine.authenticate(
            rfid_valid=True,
            face_valid=True
        )

        if result:

            logger.log(
                event="AUTHENTICATION",
                rfid="PASS",
                face="PASS",
                quantum="PASS",
                security_level=engine.level.value,
                result="GRANTED"
            )

            print("\n================================")
            print("       ACCESS GRANTED 🔓")
            print("================================")
            print(
                "Security Level :",
                engine.level.value
            )

            return

    # --------------------------------
    # QUANTUM FAILURE
    # --------------------------------

    engine.authenticate(
        rfid_valid=True,
        face_valid=True
    )

    logger.log(
        event="AUTHENTICATION",
        rfid="PASS",
        face="PASS",
        quantum="FAIL",
        security_level=engine.level.value,
        result="DENIED"
    )

    print("\n🔒 ACCESS DENIED")
    print("Security Level :", engine.level.value)


if __name__ == "__main__":
    main()