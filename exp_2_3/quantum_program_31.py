
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


def quantum_program(x, y, qc):
    a = 0
    qc.rx(0.39269908169872414, 1)
    qc.cp(0.7853981633974483, 1, 0)

    if x > -7:
        a += 1

    if y >= 17:
        a += 2
        qc.x(1)
        qc.t(1)
        qc.p(0.7853981633974483, 1)

    if check_state_gt(qc, [[0, 0.5825]], 0.01):
        return a
    else:
        return a+4

def expected_result():
    return [0,1,2,3,4,5,6,7]
    