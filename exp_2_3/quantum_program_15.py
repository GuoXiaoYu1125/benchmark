
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


def quantum_program(x, qc):
    qc.crx(1.5707963267948966, 0, 1)
    qc.cry(1.5707963267948966, 1, 0)

    if x == 6:

        if check_state_gt(qc, [[3, 0.6927]], 0.005):
            return 1
        else:
            return 2
    else:

        if check_state_gt(qc, [[3, 0.6489]], 0.01):
            return 3
        else:
            return 4

def expected_result():
    return [1, 2, 3, 4]
    