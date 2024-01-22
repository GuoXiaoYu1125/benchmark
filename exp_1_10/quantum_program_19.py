
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

def check_state_gt(qc, target_probability, delta):
    qc.measure_all()
    simulator = Aer.get_backend('aer_simulator')
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=10000).result().get_counts()
    new_job = {}
    for i in job.keys():
        new_job[int(i, 2)] = job[i]
    target = True
    for [target_state, prob] in target_probability:
        if (new_job.get(target_state, 0) / 10000) < prob - delta:
            target = False
    return target


def quantum_program(x, qc):
    qc.p(1.5707963267948966, 0)
    x -= 1
    qc.ry(1.5707963267948966, 0)
    x += 10
    x += 5
    qc.ry(0.7853981633974483, 0)
    x += 7
    qc.tdg(0)
    qc.rz(0.7853981633974483, 0)
    x -= 8
    qc.h(0)

    if x == -2:
        x -= 1
        x *= 4
        x += 9
        qc.p(0.39269908169872414, 0)
        qc.p(0.39269908169872414, 0)
        x //= 1
        qc.tdg(0)
        qc.s(0)
        qc.ry(0.39269908169872414, 0)

        if check_state_eq(qc, [0.3578, 0.6422], 0.01):
            return 1
        else:
            return 2
    else:
        qc.s(0)
        x -= 8
        qc.rz(0.7853981633974483, 0)
        x //= 1
        x //= 7
        qc.sx(0)
        qc.h(0)
        qc.tdg(0)
        qc.x(0)
        x += 1
        x *= 5
        qc.z(0)
        qc.h(0)
        qc.z(0)
        x //= 5
        x *= 6
        qc.h(0)

        if check_state_gt(qc, [[1, 0.6421]], 0.005):
            return 3
        else:
            return 4

def expected_result():
    return [1, 2, 3, 4]
    