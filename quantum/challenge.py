import hashlib

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


class QuantumChallenge:
    """
    Q-SENTINEL Quantum Security Layer

    Uses a Qiskit quantum circuit with Hadamard gates
    and quantum measurement to generate random bits.

    Current backend:
        Qiskit Aer Simulator

    IMPORTANT:
        Aer is a quantum simulator, not physical quantum hardware.
    """

    def __init__(self):

        self.backend = AerSimulator()

    # ==================================================
    # QUANTUM RANDOM BIT GENERATION
    # ==================================================

    def generate_quantum_bits(self, num_bits=128):

        circuit = QuantumCircuit(
            num_bits,
            num_bits
        )

        # Apply Hadamard gate to every qubit
        for qubit in range(num_bits):

            circuit.h(qubit)

        # Measure every qubit
        circuit.measure(
            range(num_bits),
            range(num_bits)
        )

        # Execute quantum circuit
        result = self.backend.run(
            circuit,
            shots=1
        ).result()

        counts = result.get_counts()

        measured_string = list(
            counts.keys()
        )[0]

        # Qiskit returns classical bits in reverse
        quantum_bits = measured_string[::-1]

        return quantum_bits, circuit

    # ==================================================
    # QUANTUM CHALLENGE
    # ==================================================

    def generate_challenge(self):

        quantum_bits, circuit = self.generate_quantum_bits(
            128
        )

        # Convert quantum measurement bits
        # into hexadecimal challenge
        quantum_bytes = int(
            quantum_bits,
            2
        ).to_bytes(
            16,
            byteorder="big"
        )

        challenge = quantum_bytes.hex().upper()

        return challenge, quantum_bits, circuit

    # ==================================================
    # RESPONSE GENERATION
    # ==================================================

    def generate_response(
        self,
        challenge,
        secret
    ):

        data = challenge + secret

        return hashlib.sha256(
            data.encode()
        ).hexdigest().upper()

    # ==================================================
    # RESPONSE VERIFICATION
    # ==================================================

    def verify_response(
        self,
        challenge,
        secret,
        response
    ):

        expected = self.generate_response(
            challenge,
            secret
        )

        return expected == response