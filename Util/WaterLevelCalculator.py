from PyQt5.QtCore import *
import numpy as np

class WaterLevelCalculator:
    @staticmethod
    def calculate_tap_water_level(phase_voltage):
        level = WaterLevelCalculator.solve_poly(0.00713, -0.36699, 3.7482, phase_voltage)
        return round(level, 2) if level is not None else None
    @staticmethod
    def calculate_saline_water_level(phase_voltage):
        level = WaterLevelCalculator.solve_poly(0.00755, -0.35803, 3.69399, phase_voltage)
        return round(level, 2) if level is not None else None
    @staticmethod
    def calculate_distilled_water_level(phase_voltage):
        level = WaterLevelCalculator.solve_poly(0.01135, -0.43946, 3.98331, phase_voltage)
        return round(level, 2) if level is not None else None

    @staticmethod
    def solve_poly(a, b, c, y):
        discriminant = b**2 - 4*a*(c - y)
        if discriminant >= 0:
            root1 = (-b + np.sqrt(discriminant)) / (2 * a)
            root2 = (-b - np.sqrt(discriminant)) / (2 * a)
            return root1 if 3 <= root1 <= 13 else root2 if 3 <= root2 <= 11.4 else None
        else:
            return None
    