from PyQt5.QtCore import *
import numpy as np

class WaterLevelCalculator:
    @staticmethod
    def calculate_tap_water_level(phase_voltage):
        return WaterLevelCalculator.solve_cubic(0.001, -0.034, 0.005, 2.834)

    @staticmethod
    def calculate_saline_water_level(phase_voltage):
        return WaterLevelCalculator.solve_cubic(0.001, -0.025, -0.058, 3.004)

    @staticmethod
    def calculate_distilled_water_level(phase_voltage):
        return WaterLevelCalculator.solve_cubic(0.002, -0.037, -0.010, 2.956)

    @staticmethod
    def solve_cubic(a, b, c, d, y):
        coefficients = [a, b, c, d - y]
        roots = np.roots(coefficients)
        valid_roots = [root.real for root in roots if root.imag == 0 and 0 <= root.real <= 15]
        return valid_roots[0] if valid_roots else None
    