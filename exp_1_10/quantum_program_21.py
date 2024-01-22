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
    x += 5
    qc.sxdg(0)

    if x > 20:
        a = 1
        x += 10
        qc.x(0)
        qc.sxdg(0)
        qc.t(0)
        qc.s(0)
        qc.rx(0.7853981633974483, 0)

    elif x >= 15:
        a = 2

    else:
        a = 3
        qc.sx(0)
        qc.tdg(0)
        qc.ry(0.7853981633974483, 0)

    if check_state_gt(qc, [[0, 0.4176]], 0.01):
        return a
    else:
        return a+3

def expected_result():
    return [1,2,3,4,5,6]