
from qiskit import Aer, transpile
import math

def check_state_eq(qc, target_probability, delta):
    state_len = len(target_probability)
    qubits_num = int(math.log(state_len, 2))
    qubits_state = [bin(i)[2:].zfill(qubits_num) for i in range(state_len)]
    qc.measure_all()
    simulator = Aer.get_backend('aer_simulator')
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=10000).result().get_counts()
    target = True
    for i in range(state_len):
        print(job.get(qubits_state[i], 0)/10000)
        if (job.get(qubits_state[i], 0)/10000) < target_probability[i]-delta or (job.get(qubits_state[i], 0) / 10000)> target_probability[i]+delta:
            target = False
    return target


def quantum_program(x, y, qc):
    a = 0
    qc.sdg(0)
    qc.z(0)
    qc.sx(0)
    x //= 6
    qc.tdg(0)
    qc.rz(0.39269908169872414, 0)
    qc.x(0)
    qc.p(1.5707963267948966, 0)
    x //= 5
    x //= 2
    x //= 3
    qc.y(0)

    if x > -5:
        a += 1
        qc.rz(0.39269908169872414, 0)
        qc.sx(0)
        x //= 10
        x //= 6
        qc.rx(0.39269908169872414, 0)
        qc.x(0)
        qc.t(0)
        qc.ry(1.5707963267948966, 0)
        qc.sx(0)

    if y < -13:
        a += 2
        qc.t(0)
        qc.rx(0.7853981633974483, 0)

    if check_state_eq(qc, [0.4689, 0.5311], 0.005):
        return a
    else:
        return a+4

def expected_result():
    return [0,1,2,3,4,5,6,7]
    