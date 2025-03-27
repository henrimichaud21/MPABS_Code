from PyQt5.QtCore import *
import numpy as np

class WaterLevelCalculator:
    @staticmethod
    def calculate_tap_water_level(phase_voltage):
        level = WaterLevelCalculator.solve_poly(0.00774, -0.37544, 3.77367, phase_voltage)
        return round(level, 2) if level is not None else None
    @staticmethod
    def calculate_saline_water_level(phase_voltage):
        level = WaterLevelCalculator.solve_poly(0.00806, -0.35802, 3.71559, phase_voltage)
        return round(level, 2) if level is not None else None
    @staticmethod
    def calculate_distilled_water_level(phase_voltage):
        level = WaterLevelCalculator.solve_poly(0.01066, -0.43117, 3.96147, phase_voltage)
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
    