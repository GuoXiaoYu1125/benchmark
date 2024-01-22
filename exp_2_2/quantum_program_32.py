
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

    if x <= -3:
        a += 1
        x *= 10
        qc.x(1)

    if y <= 13 and y <= -12:
        a += 2
        x += 7
        qc.cz(1, 0)
        x += 7
        qc.sxdg(0)

    if check_state_lt(qc, [[1, 0.2496]], 0.005):
        return a
    else:
        return a+4

def expected_result():
    return [0,1,2,3,4,5,6,7]