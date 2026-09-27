from quantum.challenge import QuantumChallenge


def main():

    print("================================")
    print("        Q-SENTINEL")
    print("     Quantum Security Test")
    print("================================")

    quantum = QuantumChallenge()

    print("\nGenerating quantum random bits...")

    challenge, bits, circuit = (
        quantum.generate_challenge()
    )

    print("\n================================")
    print("       QUANTUM RESULT")
    print("================================")

    print("\nBackend:")
    print("Qiskit Aer Simulator")

    print("\nQuantum Circuit:")
    print(circuit.draw())

    print("\nQuantum Random Bits:")
    print(bits)

    print("\nNumber of Bits:")
    print(len(bits))

    print("\nQuantum Challenge:")
    print(challenge)

    secret = "Q_SENTINEL_SECRET"

    response = quantum.generate_response(
        challenge,
        secret
    )

    verified = quantum.verify_response(
        challenge,
        secret,
        response
    )

    print("\nResponse:")
    print(response)

    print(
        "\nVerification:",
        "PASSED ✅" if verified else "FAILED ❌"
    )

    print("\n================================")
    print(" Quantum Test Completed")
    print("================================")


if __name__ == "__main__":
    main()