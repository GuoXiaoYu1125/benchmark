
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


def quantum_program(x, y, qc):
    a = 0
    x *= 5
    qc.tdg(0)
    qc.x(0)

    if x == -11:
        a += 1
        qc.z(0)
        x //= 6
        qc.y(0)
        qc.h(0)
        qc.p(0.39269908169872414, 0)

    if y == 5:
        a += 2
        x += 7
        qc.sx(0)
        x -= 6
        x //= 10
        qc.x(0)

    if check_state_eq(qc, [0.424, 0.576], 0.005):
        return a
    else:
        return a+4

def expected_result():
    return [0,1,2,3,4,5,6,7]
    