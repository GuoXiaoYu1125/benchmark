
from qiskit import Aer, transpile
import math

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

    if x < -3:
        qc.crx(1.5707963267948966, 1, 0)

        if check_state_lt(qc, [[3, 0.22], [2, 0.1371]], 0.01):
            return 1
        else:
            return 2
    else:
        qc.p(1.5707963267948966, 1)
        qc.crx(1.5707963267948966, 0, 1)

        if check_state_gt(qc, [[3, 0.4006]], 0.005):
            return 3
        else:
            return 4

def expected_result():
    return [1, 2, 3, 4]
    