
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
    a = 0
    x -= 3
    qc.p(0.39269908169872414, 1)

    if x <= -12:
        a = 1
        qc.sx(1)
        x -= 8
        qc.cp(1.5707963267948966, 1, 0)

    elif x > -12:
        a = 2
        qc.cs(1, 0)
        qc.sdg(0)

    else:
        a = 3
        x -= 10
        qc.t(1)

    if x == -5 or check_state_gt(qc, [[0, 0.4992]], 0.01):
        return a
    else:
        return a+3

def expected_result():
    return [1,2,3,4,5,6]
    