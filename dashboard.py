import streamlit as st
from datetime import datetime

from controller.security_controller import QSentinelController
from quantum.challenge import QuantumChallenge
from face_verification.face_auth import verify_face


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Q-SENTINEL",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PREMIUM DARK UI
# ============================================================

st.markdown("""
<style>

@import url(
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(59,130,246,0.12),
            transparent 25%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(139,92,246,0.10),
            transparent 25%
        ),
        #070b14;

    color: #f8fafc;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background: #0a0f1c;
    border-right: 1px solid #1e293b;
}

section[data-testid="stSidebar"] h1 {
    color: #ffffff;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    padding: 10px 0 25px 0;
}

.quantum-badge {
    display: inline-block;

    background: rgba(99,102,241,0.15);

    border: 1px solid rgba(129,140,248,0.35);

    color: #a5b4fc;

    padding: 6px 12px;

    border-radius: 20px;

    font-size: 12px;

    font-weight: 700;

    margin-bottom: 10px;
}

.hero-title {
    font-size: 40px;

    font-weight: 800;

    letter-spacing: -1.5px;

    margin-bottom: 5px;
}

.hero-subtitle {
    color: #94a3b8;

    font-size: 15px;
}


/* ============================================================
   CARDS
   ============================================================ */

.card {
    background:
        linear-gradient(
            145deg,
            rgba(15,23,42,0.96),
            rgba(9,14,26,0.96)
        );

    border: 1px solid #1e293b;

    border-radius: 18px;

    padding: 20px;

    min-height: 145px;

    box-shadow:
        0 12px 35px rgba(0,0,0,0.18);
}

.card-title {
    color: #94a3b8;

    font-size: 12px;

    font-weight: 600;

    text-transform: uppercase;

    letter-spacing: 1px;
}

.card-value {
    color: #f8fafc;

    font-size: 25px;

    font-weight: 800;

    margin-top: 12px;
}

.card-small {
    color: #64748b;

    font-size: 12px;

    margin-top: 7px;
}


/* ============================================================
   STATUS COLORS
   ============================================================ */

.status-normal {
    color: #34d399;
}

.status-warning {
    color: #fbbf24;
}

.status-lockdown {
    color: #f87171;
}


/* ============================================================
   QUANTUM PANEL
   ============================================================ */

.quantum-panel {
    background:
        linear-gradient(
            135deg,
            rgba(30,41,59,0.95),
            rgba(15,23,42,0.95)
        );

    border: 1px solid #334155;

    border-radius: 20px;

    padding: 24px;
}

.quantum-title {
    font-size: 20px;

    font-weight: 800;
}

.quantum-subtitle {
    color: #94a3b8;

    font-size: 13px;

    margin-top: 5px;
}


/* ============================================================
   ACCESS RESULT
   ============================================================ */

.access-granted {
    background:
        rgba(16,185,129,0.08);

    border:
        1px solid rgba(52,211,153,0.35);

    color: #34d399;

    border-radius: 18px;

    padding: 25px;

    text-align: center;

    font-size: 25px;

    font-weight: 800;
}

.access-denied {
    background:
        rgba(239,68,68,0.08);

    border:
        1px solid rgba(248,113,113,0.35);

    color: #f87171;

    border-radius: 18px;

    padding: 25px;

    text-align: center;

    font-size: 25px;

    font-weight: 800;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {

    width: 100%;

    border-radius: 10px;

    border: 1px solid #334155;

    background: #111827;

    color: #f8fafc;

    font-weight: 600;

    min-height: 42px;
}

.stButton > button:hover {

    border-color: #6366f1;

    color: white;
}


/* ============================================================
   DIVIDER
   ============================================================ */

hr {
    border-color: #1e293b;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "system" not in st.session_state:

    st.session_state.system = (
        QSentinelController()
    )


if "quantum_data" not in st.session_state:

    st.session_state.quantum_data = None


if "last_event" not in st.session_state:

    st.session_state.last_event = (
        "System initialized"
    )


if "rfid" not in st.session_state:

    st.session_state.rfid = False


if "face" not in st.session_state:

    st.session_state.face = False


if "quantum" not in st.session_state:

    st.session_state.quantum = False


if "access" not in st.session_state:

    st.session_state.access = False


system = st.session_state.system


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🛡️ Q-SENTINEL")

    st.caption(
        "Quantum-Adaptive Physical Security"
    )

    st.divider()

    # --------------------------------------------------------
    # SYSTEM
    # --------------------------------------------------------

    st.markdown("### SYSTEM")

    if st.button("🔄 Reset System"):

        system.reset_system()

        st.session_state.rfid = False

        st.session_state.face = False

        st.session_state.quantum = False

        st.session_state.access = False

        st.session_state.quantum_data = None

        st.session_state.last_event = (
            "System reset"
        )

        st.rerun()


    # --------------------------------------------------------
    # AUTHENTICATION
    # --------------------------------------------------------

    st.markdown("### AUTHENTICATION")


    # RFID
    if st.button("🪪 Verify RFID"):

        result = system.verify_rfid(
            "Q-SENTINEL-USER-01"
        )

        st.session_state.rfid = result

        if result:

            st.session_state.last_event = (
                "RFID verification passed"
            )

        else:

            st.session_state.last_event = (
                "RFID verification failed"
            )

        st.rerun()


    # REAL CAMERA FACE
    if st.button("📷 Verify Face"):

        with st.spinner(
            "Opening camera for face authentication..."
        ):

            result = verify_face(
                show_camera=True
            )

        st.session_state.face = result

        if result:

            st.session_state.last_event = (
                "Face verification passed"
            )

        else:

            st.session_state.last_event = (
                "Face verification failed"
            )

        st.rerun()


    # QUANTUM
    if st.button(
        "⚛️ Generate Quantum Challenge"
    ):

        quantum = QuantumChallenge()

        (
            challenge,
            bits,
            circuit
        ) = quantum.generate_challenge()

        st.session_state.quantum_data = {

            "challenge": challenge,

            "bits": bits,

            "circuit": circuit
        }

        st.session_state.quantum = True

        st.session_state.last_event = (
            "Quantum challenge generated"
        )

        st.rerun()


    # FINAL AUTHENTICATION
    if st.button(
        "🔓 Run Authentication"
    ):

        result = system.authenticate(

            rfid_valid=(
                st.session_state.rfid
            ),

            face_valid=(
                st.session_state.face
            ),

            quantum_valid=(
                st.session_state.quantum
            )
        )

        st.session_state.access = result

        if result:

            st.session_state.last_event = (
                "ACCESS GRANTED"
            )

        else:

            st.session_state.last_event = (
                "ACCESS DENIED"
            )

        st.rerun()


    # --------------------------------------------------------
    # SECURITY
    # --------------------------------------------------------

    st.markdown("### SECURITY TEST")


    if st.button("🚨 Trigger Tamper"):

        state = system.check_tamper(

            door_open=True,

            vibration=True
        )

        st.session_state.last_event = (
            f"Tamper event detected: {state}"
        )

        st.rerun()


    if st.button("🔐 Admin Recovery"):

        result = system.admin_recovery(

            admin_id="Q-ADMIN-01",

            admin_password="QADMIN-2026"
        )

        if result:

            st.session_state.last_event = (
                "Admin recovery successful"
            )

        else:

            st.session_state.last_event = (
                "Admin recovery denied"
            )

        st.rerun()


# ============================================================
# HEADER
# ============================================================

st.markdown(
"""
<div class="hero">

<div class="quantum-badge">
QUANTUM SECURITY SYSTEM
</div>

<div class="hero-title">
Q-SENTINEL
</div>

<div class="hero-subtitle">
Quantum-Adaptive Physical Security & Zero-Trust Access Control
</div>

</div>
""",
unsafe_allow_html=True
)


# ============================================================
# SYSTEM STATUS
# ============================================================

status = system.status()

overall = status["overall_state"]

tamper = status["tamper"]["state"]

failed = status["security"]["failed_attempts"]


if overall == "NORMAL":

    overall_class = "status-normal"

elif overall == "HIGH":

    overall_class = "status-warning"

else:

    overall_class = "status-lockdown"


# ============================================================
# TOP STATUS CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)


# SYSTEM STATUS
with c1:

    st.markdown(
    f"""
    <div class="card">

    <div class="card-title">
    System Status
    </div>

    <div class="card-value {overall_class}">
    ● {overall}
    </div>

    <div class="card-small">
    Security engine state
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )


# QUANTUM
with c2:

    st.markdown(
    """
    <div class="card">

    <div class="card-title">
    Quantum Layer
    </div>

    <div class="card-value status-normal">
    ⚛ ACTIVE
    </div>

    <div class="card-small">
    Qiskit Aer Simulator
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )


# TAMPER
with c3:

    tamper_class = (
        "status-normal"
        if tamper == "NORMAL"
        else "status-lockdown"
    )

    st.markdown(
    f"""
    <div class="card">

    <div class="card-title">
    Tamper Monitor
    </div>

    <div class="card-value {tamper_class}">
    ● {tamper}
    </div>

    <div class="card-small">
    Events: {status["tamper"]["tamper_events"]}
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )


# FAILED ATTEMPTS
with c4:

    st.markdown(
    f"""
    <div class="card">

    <div class="card-title">
    Failed Attempts
    </div>

    <div class="card-value">
    {failed}
    </div>

    <div class="card-small">
    Lock threshold: 3
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )


st.write("")


# ============================================================
# AUTHENTICATION PIPELINE
# ============================================================

st.markdown(
    "### Authentication Pipeline"
)


a1, a2, a3 = st.columns(3)


# RFID
with a1:

    text = (
        "VERIFIED"
        if st.session_state.rfid
        else "WAITING"
    )

    css = (
        "status-normal"
        if st.session_state.rfid
        else ""
    )

    st.markdown(
    f"""
    <div class="card">

    <div class="card-title">
    Factor 01
    </div>

    <div class="card-value">
    🪪 RFID
    </div>

    <div class="card-small {css}">
    ● {text}
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )


# FACE
with a2:

    text = (
        "VERIFIED"
        if st.session_state.face
        else "WAITING"
    )

    css = (
        "status-normal"
        if st.session_state.face
        else ""
    )

    st.markdown(
    f"""
    <div class="card">

    <div class="card-title">
    Factor 02
    </div>

    <div class="card-value">
    🧬 FACE
    </div>

    <div class="card-small {css}">
    ● {text}
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )


# QUANTUM
with a3:

    text = (
        "VERIFIED"
        if st.session_state.quantum
        else "WAITING"
    )

    css = (
        "status-normal"
        if st.session_state.quantum
        else ""
    )

    st.markdown(
    f"""
    <div class="card">

    <div class="card-title">
    Factor 03
    </div>

    <div class="card-value">
    ⚛ QUANTUM
    </div>

    <div class="card-small {css}">
    ● {text}
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )


st.write("")


# ============================================================
# QUANTUM SECURITY ENGINE
# ============================================================

st.markdown(
"""
<div class="quantum-panel">

<div class="quantum-title">
⚛ Quantum Security Engine
</div>

<div class="quantum-subtitle">
Dynamic challenge generation using Qiskit quantum circuit simulation
</div>

</div>
""",
unsafe_allow_html=True
)


if st.session_state.quantum_data:

    data = st.session_state.quantum_data

    q1, q2 = st.columns([1, 2])


    with q1:

        st.metric(
            "Quantum Backend",
            "Aer Simulator"
        )

        st.metric(
            "Qubits",
            "128"
        )

        st.metric(
            "Quantum Gate",
            "Hadamard"
        )


    with q2:

        st.markdown(
            "#### Dynamic Quantum Challenge"
        )

        st.code(
            data["challenge"],
            language="text"
        )

        st.markdown(
            "**Quantum Random Bits — First 32 Bits**"
        )

        st.code(
            data["bits"][:32],
            language="text"
        )


else:

    st.info(
        "Generate a quantum challenge from the "
        "sidebar to activate the quantum security layer."
    )

# ============================================================
# QUANTUM CIRCUIT VISUALIZATION
# ============================================================

st.write("")

st.markdown("### Quantum Circuit")

if st.session_state.quantum_data:

    circuit = st.session_state.quantum_data["circuit"]

    st.markdown(
        """
        <div class="quantum-panel">

        <div class="quantum-title">
        ⚛ Live Quantum Circuit
        </div>

        <div class="quantum-subtitle">
        Hadamard gates create quantum superposition,
        followed by measurement to generate the challenge.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Compact visual circuit
    # --------------------------------------------------------

    from qiskit import QuantumCircuit

    visual_circuit = QuantumCircuit(8, 8)

    for qubit in range(8):

        visual_circuit.h(qubit)

    visual_circuit.measure(
        range(8),
        range(8)
    )

    st.code(
        visual_circuit.draw(),
        language="text"
    )

    st.caption(
        "Visualization shows the first 8 qubits. "
        "The security challenge is generated using the "
        "full 128-qubit quantum circuit."
    )

else:

    st.info(
        "Generate a quantum challenge to display "
        "the quantum circuit."
    )
# ============================================================
# ACCESS DECISION
# ============================================================

st.write("")

st.markdown(
    "### Access Decision"
)


if st.session_state.access:

    st.markdown(
    """
    <div class="access-granted">

    🔓 ACCESS GRANTED

    <div style="
        font-size:13px;
        font-weight:500;
        margin-top:8px;
    ">

    All authentication factors verified

    </div>

    </div>
    """,
    unsafe_allow_html=True
    )

else:

    st.markdown(
    """
    <div class="access-denied">

    🔒 ACCESS DENIED

    <div style="
        font-size:13px;
        font-weight:500;
        margin-top:8px;
    ">

    Authentication required

    </div>

    </div>
    """,
    unsafe_allow_html=True
    )


# ============================================================
# LATEST EVENT
# ============================================================

st.write("")

e1, e2 = st.columns([2, 1])


with e1:

    st.markdown(
        "### Latest Security Event"
    )

    st.info(
        st.session_state.last_event
    )


with e2:

    st.markdown(
        "### System Time"
    )

    st.metric(
        "Last Update",
        datetime.now().strftime(
            "%H:%M:%S"
        )
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Q-SENTINEL • Quantum-Adaptive Physical Security • "
    "Qiskit Aer Simulation • Zero-Trust Architecture"
)