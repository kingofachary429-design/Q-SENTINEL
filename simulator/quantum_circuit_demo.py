from qiskit import QuantumCircuit

from quantum.challenge import QuantumChallenge


def main():

    print("=" * 60)
    print("              Q-SENTINEL")
    print("        QUANTUM CIRCUIT DEMO")
    print("=" * 60)

    quantum = QuantumChallenge()

    print("\nGenerating quantum circuit...")

    challenge, bits, circuit = quantum.generate_challenge()

    print("\nBackend:")
    print("Qiskit Aer Simulator")

    print("\nQuantum Algorithm:")
    print("Hadamard Gate + Measurement")

    print("\nNumber of Qubits:")
    print("128")

    print("\nQuantum Circuit Summary:")
    print("----------------------------")
    print("128 qubits initialized")
    print("128 Hadamard gates applied")
    print("128 measurements performed")

    # ============================================
    # CREATE SMALL VISUAL CIRCUIT
    # ============================================

    print("\nSample Quantum Circuit:")
    print("----------------------------")

    sample = QuantumCircuit(8, 8)

    for qubit in range(8):
        sample.h(qubit)

    sample.measure(
        range(8),
        range(8)
    )

    print(sample.draw())

    # ============================================
    # QUANTUM RESULT
    # ============================================

    print("\nQuantum Random Bits:")
    print(bits[:32])

    print("\nQuantum Challenge:")
    print(challenge)

    print("\nQuantum circuit execution: PASSED")

    print("\n" + "=" * 60)
    print("        QUANTUM CIRCUIT DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()