
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
    qc.s(0)
    qc.y(0)
    x -= 6
    qc.x(0)
    x *= 5
    qc.rx(0.39269908169872414, 0)
    qc.h(0)

    if x >= 9:
        a += 1
        qc.ry(0.7853981633974483, 0)
        x += 7
        x *= 10
        qc.sdg(0)
        qc.rx(0.39269908169872414, 0)
        qc.y(0)
        x -= 5
        x *= 10
        qc.s(0)
        qc.sdg(0)
        qc.x(0)
        qc.t(0)
        x *= 3
        qc.rz(0.39269908169872414, 0)

    else:
        a -=1
        qc.t(0)

    if check_state_gt(qc, [[1, 0.5035]], 0.005):
        return a
    else:
        return a+1
        
def expected_result():
    return [-1, 0, 1, 2]
    