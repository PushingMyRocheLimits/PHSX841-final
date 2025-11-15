import numpy as np

class Material:
    # Material properties used by the toy physics.
    # Fields (typical units): density (g/cm3), X0 (radiation length, cm), lambda_int (int. length for hadrons, cm)

    def __init__(self, name, density, X0, lambda_int):
        self.name = name
        self.density = density
        self.X0 = X0
        self.lambda_int = lambda_int
