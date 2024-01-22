
from qiskit import Aer, transpile
import math

def check_state_eq(qc, target_probability, delta):
    state_len = len(target_probability)
    qubits_num = int(math.log(state_len, 2))
    qubits_state = [bin(i)[2:].zfill(qubits_num) for i in range(state_len)]
    qc.measure_all()
    simulator = Aer.get_backend('aer_simulator')
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=10000).result().get_counts()
    target = True
    for i in range(state_len):
        print(job.get(qubits_state[i], 0)/10000)
        if (job.get(qubits_state[i], 0)/10000) < target_probability[i]-delta or (job.get(qubits_state[i], 0) / 10000)> target_probability[i]+delta:
            target = False
    return target


def quantum_program(x, qc):
    x *= 8
    qc.ry(0.39269908169872414, 0)
    qc.rz(0.7853981633974483, 0)

    if x > 15:
        qc.y(0)
        x -= 7
        qc.t(0)
        qc.sdg(0)

        if check_state_eq(qc, [0.7218, 0.2782], 0.01):
            return 1
        else:
            return 2
    else:

        if check_state_eq(qc, [0.2225, 0.7775], 0.01):
            return 3
        else:
            return 4

def expected_result():
    return [1, 2, 3, 4]
    