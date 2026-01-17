from setuptools import setup, find_packages

setup(
    name="quantum-ml",
    version="0.1.0",
    description="Quantum Machine Learning Module",
    packages=find_packages(),
    install_requires=[
        "quantum-compute",
        "torch",
        "pennylane",
        "numpy"
    ],
)
