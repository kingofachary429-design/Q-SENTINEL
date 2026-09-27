from quantum.challenge import QuantumChallenge


def main():

    print("=" * 55)
    print("              Q-SENTINEL")
    print("        QUANTUM SECURITY DEMO")
    print("=" * 55)

    quantum = QuantumChallenge()

    # Generate quantum challenge
    print("\n[1] QUANTUM RANDOMNESS")
    print("-" * 55)

    challenge, bits, circuit = quantum.generate_challenge()

    print("Backend       : Qiskit Aer Simulator")
    print("Qubits        : 128")
    print("Gate          : Hadamard (H)")
    print("Measurement   : Quantum Measurement")

    print("\nFirst 32 Quantum Bits:")
    print(bits[:32])

    print("\nQuantum Challenge:")
    print(challenge)

    # Show compact circuit information
    print("\n[2] QUANTUM CIRCUIT")
    print("-" * 55)

    print("Quantum Circuit Generated Successfully")
    print("Operation     : H gates + Measurement")
    print("Circuit Size  : 128 Qubits")

    # Generate response
    print("\n[3] CHALLENGE-RESPONSE")
    print("-" * 55)

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

    print("Challenge     :", challenge)
    print("Response      :", response[:32] + "...")
    print(
        "Verification  :",
        "PASSED" if verified else "FAILED"
    )

    # Final result
    print("\n[4] QUANTUM SECURITY RESULT")
    print("-" * 55)

    if verified:
        print("Quantum Layer : ACTIVE")
        print("Randomness    : QUANTUM")
        print("Challenge     : VALID")
        print("Authentication: PASSED")
        print("Access Status : GRANTED")
    else:
        print("Quantum Layer : FAILED")
        print("Access Status : DENIED")

    print("\n" + "=" * 55)
    print("       QUANTUM SECURITY DEMO COMPLETED")
    print("=" * 55)


if __name__ == "__main__":
    main()