
from qiskit import Aer, transpile
import math

def check_state_lt(qc, target_probability, delta):
    qc.measure_all()
    simulator = Aer.get_backend('aer_simulator')
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=10000).result().get_counts()
    new_job = {}
    for i in job.keys():
        new_job[int(i, 2)] = job[i]
    target = True
    for [target_state, prob] in target_probability:
        if (new_job.get(target_state, 0) / 10000) > prob + delta:
            target = False
    return target


def quantum_program(x, qc):
    x -= 7
    qc.y(0)
    x *= 10
    qc.h(0)
    qc.x(0)
    x *= 5
    qc.z(0)

    if x <= -1:
        qc.t(0)
        qc.h(0)
        x -= 8
        x -= 5
        x += 6
        x //= 3
        qc.y(0)
        x += 2
        qc.y(0)
        qc.rz(1.5707963267948966, 0)

        if check_state_lt(qc, [[1, 0.36]], 0.01):
            return 1
        else:
            return 2
    else:
        x *= 2
        x -= 10
        x *= 3
        qc.x(0)

        if check_state_lt(qc, [[0, 0.4905]], 0.005):
            return 3
        else:
            return 4

def expected_result():
    return [1, 2, 3, 4]
    