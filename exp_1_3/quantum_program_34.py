
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
    x -= 8
    x -= 1
    qc.sx(0)

    if x != 13:
        a += 1

    if y <= 13:
        a += 2
        x //= 8
        qc.t(0)
        qc.tdg(0)
        qc.tdg(0)

    if check_state_gt(qc, [[0, 0.6328]], 0.01):
        return a
    else:
        return a+4

def expected_result():
    return [0,1,2,3,4,5,6,7]
    