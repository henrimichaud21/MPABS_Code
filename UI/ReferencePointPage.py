import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ReferencePointPage(QWidget):

    referenceChanged = pyqtSignal(str)
    def __init__(self, current_reference="0"):
        super().__init__()
        self.setGeometry(1000, 100, 450, 150)
        self.setWindowTitle("Change Reference Point Page")

        # Create "Change reference point to:" label
        self.referenceLabel = QLabel("Change reference point to (between 3 and 11):", self)
        self.referenceLabel.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.referenceLabel.setFixedSize(450, 30)
        self.referenceLabel.move(10,10)

        # Create input field and "cm" label
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter value")
        self.input_field.setStyleSheet("font-size: 16px")
        self.input_field.setFixedSize(100, 30)
        self.input_field.move(10,40)
        

        self.cmLabel = QLabel("cm", self)
        self.cmLabel.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.cmLabel.setFixedSize(50, 30)
        self.cmLabel.move(120, 40)

        # Create Apply button
        self.apply_btn = QPushButton("Apply", self)
        self.apply_btn.setStyleSheet("font-size: 16px")
        self.apply_btn.clicked.connect(self.apply_action)
        self.apply_btn.setFixedSize(100, 30)
        self.apply_btn.move(10, 80)

        # Create Cancel button
        self.cancel_btn = QPushButton("Cancel", self)
        self.cancel_btn.setStyleSheet("font-size: 16px")
        self.cancel_btn.clicked.connect(self.cancel_action)
        self.cancel_btn.setFixedSize(100, 30)
        self.cancel_btn.move(120, 80)

    def apply_action(self):
        input_value = self.input_field.text()
        if input_value.isdigit():  # Ensure input is a valid number
            self.referenceChanged.emit(str(int(input_value)))  # Convert to int, then back to string for signal
        else:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number.")
        self.close()

    def cancel_action(self):
        # Handle Cancel button click
        print("Action cancelled")
        self.close()  # Close the page