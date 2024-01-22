
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
    qc.cp(1.5707963267948966, 0, 1)
    qc.cs(1, 0)

    if x == 12:
        a = 1
        qc.z(0)

    elif x <= -19:
        a = 2
        qc.cp(0.39269908169872414, 1, 0)
        x += 7
        qc.tdg(0)
        qc.y(0)

    else:
        a = 3
        qc.sxdg(0)
        x //= 5
        qc.iswap(1, 0)
        qc.rx(0.7853981633974483, 1)

    if check_state_lt(qc, [[3, 0.12], [1, 0.1259]], 0.01):
        return a
    else:
        return a+3

def expected_result():
    return [1,2,3,4,5,6]
    