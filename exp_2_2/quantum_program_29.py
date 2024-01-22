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
    qc.iswap(1, 0)

    if x <= 11:
        a = 1
        x //= 7
        qc.cry(0.39269908169872414, 0, 1)

    elif x > -17 or x < 6:
        a = 2

    else:
        a = 3
        qc.cz(1, 0)

    if check_state_gt(qc, [[3, 0.6732]], 0.005):
        return a
    else:
        return a+3

def expected_result():
    return [1,2,3,4,5,6]