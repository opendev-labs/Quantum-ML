import torch
from quantum_compute import QuantumDevice
from .quantum_model import QuantumMLModel, circuit_fn
from pydantic import BaseModel

# In a real scenario, we might import this from Quantum-API or run it standalone.
# But since this file was acting as a mini-server/script, we update it to use the new model.

# Define quantum device again or reuse from model if exported (cleaner to reuse)
# For now, we just demonstrate usages.

class InputValue(BaseModel):
    input_value: float

def predict(input_value: float):
    # Using the circuit function from quantum_model
    # We map the single input value to the weights expected by the circuit
    # This is a simplification to match previous logic
    weights = [input_value, input_value] 
    
    quantum_result = circuit_fn(weights)
    
    classical_model = QuantumMLModel()
    
    # Adjust shape
    input_tensor = torch.tensor([[quantum_result, quantum_result, quantum_result]], dtype=torch.float32)
    
    classical_result = classical_model(input_tensor)
    
    return {"quantum_result": float(quantum_result), "classical_result": classical_result.item()}

if __name__ == "__main__":
    print(predict(0.5))
