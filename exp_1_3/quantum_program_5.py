
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
    a = 0
    x += 6
    x //= 8
    qc.z(0)

    if x <= -19:
        a += 1
        qc.h(0)

    else:
        a -=1
        qc.t(0)
        qc.z(0)
        qc.y(0)

    if check_state_lt(qc, [[0, 0.2262]], 0.01):
        return a
    else:
        return a+1
        
def expected_result():
    return [-1, 0, 1, 2]
    