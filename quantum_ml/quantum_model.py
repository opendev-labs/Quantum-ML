import torch
import numpy as np
import pennylane as qml
from quantum_compute import QuantumDevice, QuantumCircuit

# Define the quantum device using our new wrapper
device_wrapper = QuantumDevice(wires=3)

class CustomQuantumCircuit(QuantumCircuit):
    """
    Specific Quantum Circuit for the ML Model.
    """
    def create_circuit(self):
        @qml.qnode(self.dev)
        def circuit(weights):
            qml.Hadamard(wires=0)
            qml.RX(weights[0], wires=1)
            qml.RY(weights[1], wires=2)
            
            # Entanglement
            qml.CNOT(wires=[0, 1])
            qml.CNOT(wires=[1, 2])
            
            return qml.expval(qml.PauliZ(0))
        return circuit

# Initialize circuit
q_circuit = CustomQuantumCircuit(device_wrapper)
circuit_fn = q_circuit.create_circuit()

# Define hybrid classical-quantum model
class QuantumMLModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(3, 1)

    def forward(self, x):
        return self.linear(x)

# Function to use quantum output
def hybrid_model(weights):
    quantum_output = circuit_fn(weights)
    classical_input = torch.tensor([[quantum_output]], dtype=torch.float32)
    return classical_input

def optimize_model():
    model = QuantumMLModel()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    for epoch in range(100):
        weights = np.random.rand(3)
        optimizer.zero_grad()
        loss = model(hybrid_model(weights))
        loss.backward()
        optimizer.step()
    return model
