
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
    qc.t(0)
    qc.z(0)
    x += 4
    qc.ry(1.5707963267948966, 0)
    qc.z(0)
    qc.t(0)

    if x >= -4:
        x -= 5
        x //= 10
        qc.p(0.39269908169872414, 0)
        x *= 5
        qc.tdg(0)

        if check_state_eq(qc, [0.2387, 0.7613], 0.01):
            return 1
        else:
            return 2
    else:
        x //= 10
        x //= 9
        x += 5
        qc.x(0)

        if check_state_eq(qc, [0.629, 0.371], 0.01):
            return 3
        else:
            return 4

def expected_result():
    return [1, 2, 3, 4]
    