
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
    a = 0

    if x <= -14:
        a = 1
        qc.swap(1, 0)

    elif x < -10:
        a = 2
        qc.crx(0.7853981633974483, 1, 0)
        x += 5
        qc.rz(0.39269908169872414, 1)

    else:
        a = 3
        qc.cz(0, 1)
        x *= 10
        qc.h(1)

    if check_state_eq(qc, [0.374, 0.4399, 0.0473, 0.1389], 0.005):
        return a
    else:
        return a+3

def expected_result():
    return [1,2,3,4,5,6]
    