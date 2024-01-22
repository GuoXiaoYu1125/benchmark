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
    qc.sxdg(0)

    if x != 12:
        qc.sx(0)
        x //= 7
        x += 1
        qc.sxdg(0)
        qc.x(0)
        qc.rx(1.5707963267948966, 0)

        if check_state_lt(qc, [[1, 0.3053]], 0.005):
            return 1
        else:
            return 2
    else:
        qc.rx(0.7853981633974483, 0)
        qc.t(0)
        qc.rz(0.39269908169872414, 0)
        qc.h(0)

        if check_state_lt(qc, [[1, 0.4905]], 0.005):
            return 3
        else:
            return 4

def expected_result():
    return [1, 2, 3, 4]