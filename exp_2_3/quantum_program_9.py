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

    if x >= -5:
        a += 1

    else:
        a -=1
        qc.csdg(1, 0)

    if check_state_lt(qc, [[0, 0.218], [2, 0.2166]], 0.005):
        return a
    else:
        return a+1
        
def expected_result():
    return [-1, 0, 1, 2]