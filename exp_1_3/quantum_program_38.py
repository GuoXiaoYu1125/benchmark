
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


def quantum_program(x, y, qc):
    a = 0

    if x <= -18:
        a += 1
        qc.x(0)
        qc.h(0)

    if y > -3:
        a += 2
        qc.rz(1.5707963267948966, 0)
        qc.y(0)
        qc.t(0)

    if check_state_lt(qc, [[1, 0.3336]], 0.01):
        return a
    else:
        return a+4

def expected_result():
    return [0,1,2,3,4,5,6,7]
    