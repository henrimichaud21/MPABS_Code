import sys
import threading
import serial.tools.list_ports
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from UI.FullDataPage import FullDataPage
from UI.ReferencePointPage import ReferencePointPage
from Threading.SerialThread import SerialThread
from Util.WaterLevelCalculator import WaterLevelCalculator
from datetime import datetime
from PyQt5.QtCore import *

def setup_toggle_button(button, phrase1, phrase2, home_page_instance):
    button.setCheckable(True)

    def toggle_button():
        if button.isChecked():
            button.setStyleSheet("background-color: green")
            button.setText(phrase1)
            home_page_instance.start_serial_thread()

        else:
            button.setChecked(False)
            button.setStyleSheet("")
            button.setText(phrase2)
            home_page_instance.stop_serial_thread()

        if button == home_page_instance.record_btn:
            home_page_instance.full_data_page.sync_toggle_button(button.isChecked())

    button.clicked.connect(toggle_button)

class HomePage(QWidget):
    update_toggle_button_signal = pyqtSignal(bool)
    def __init__(self):
        # Create Window
        super().__init__()
        self.setGeometry(1200, 300, 750, 750)
        self.setWindowTitle("Microstrip Patch Antenna Home Screen")

        # Add TextFields
        self.antennaLabel = QLabel("Antenna 1 Status: ", self)
        self.antennaLabel.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.antennaLabel.setFixedSize(200, 30)
        self.antennaLabel.move(10,10)

        self.connectionLabel = QLabel("Not Connected", self)
        self.connectionLabel.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.connectionLabel.setFixedSize(200,30)
        self.connectionLabel.move(250,10)

        self.solutionLabel = QLabel("Select Solution Type:", self)
        self.solutionLabel.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.solutionLabel.setFixedSize(200,30)
        self.solutionLabel.move(10,120)

        self.timeLastReadingLabel = QLabel("Time since last reading: xx:xx:xx", self)
        self.timeLastReadingLabel.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.timeLastReadingLabel.setFixedSize(500,30)
        self.timeLastReadingLabel.move(10,200)

        self.valueLastReadingLabel = QLabel("Value of last reading: x cm", self)
        self.valueLastReadingLabel.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.valueLastReadingLabel.setFixedSize(250,30)
        self.valueLastReadingLabel.move(10,220)

        # Add checkbox
        self.connectionCheckbox = QCheckBox("", self)
        self.connectionCheckbox.setFixedSize(30,30)
        self.connectionCheckbox.move(200,10)

        # Add Record Button
        self.record_btn = QPushButton("Start Recording Data", self)
        self.record_btn.setFixedSize(200, 50)
        self.record_btn.move(220, 150)
        self.record_btn.setStyleSheet("font-size: 16px")
        setup_toggle_button(self.record_btn, "Stop Recording Data", "Start Recording Data", self)

        # Add View Full Data Button
        self.dataPage_btn = QPushButton("View Full Data", self)
        self.dataPage_btn.setStyleSheet("font-size: 16px")
        self.dataPage_btn.setFixedSize(200, 50)
        self.dataPage_btn.move(430, 150)
        self.dataPage_btn.clicked.connect(self.open_data_page)

        # Dropdown
        self.solutionDropdown = QComboBox(self)
        self.solutionDropdown.addItems(["Saline Solution", "Distilled Solution", "Tap Solution"])
        self.solutionDropdown.setStyleSheet("font-size: 16px")
        self.solutionDropdown.setFixedSize(200, 50)
        self.solutionDropdown.move(10, 150)
        self.selected_solution = self.solutionDropdown.currentText()
        self.solutionDropdown.currentTextChanged.connect(self.update_solution_in_fulldata)

        # Enter Reference Point Button
        self.referencepoint_btn = QPushButton("Enter Reference Point", self)
        self.referencepoint_btn.setStyleSheet("font-size: 16px")
        self.referencepoint_btn.setFixedSize(175, 50)
        self.referencepoint_btn.move(10, 55)
        self.referencepoint_btn.clicked.connect(self.open_reference_page)

        # Reference Point Label
        self.current_reference_point = 0
        self.currentReferenceLabel = QLabel(f"Current Reference Point: {self.current_reference_point} cm", self)
        self.currentReferenceLabel.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.currentReferenceLabel.setFixedSize(275,30)
        self.currentReferenceLabel.move(195,65)

        # Start Serial Communication
        self.serial_thread = None
        self.thread = None

        self.full_data_page = FullDataPage(self.current_reference_point, self.selected_solution)
        self.full_data_page.stop_recording_signal.connect(self.handle_stop_recording)


        self.recorded_data = []

        # Start the timer to check FTDI connection periodically
        self.connectionTimer = QTimer(self)
        self.connectionTimer.timeout.connect(self.check_ftdi_connection)
        self.connectionTimer.start(500)  # Check every 500 miliseconds

        # Run once at startup to set initial state
        self.check_ftdi_connection()

    def handle_stop_recording(self, is_recording):
        if not is_recording:
            self.record_btn.setText("Start Recording Data")
            self.record_btn.setChecked(False)
            self.record_btn.setStyleSheet("")
            self.stop_serial_thread()
        else:
            self.selected_solution = self.solutionDropdown.currentText()
            self.record_btn.setText("Stop Recording Data")
            self.record_btn.setStyleSheet("background-color: green")
            self.record_btn.setChecked(True)
            self.start_serial_thread()

        if self.full_data_page:
            self.full_data_page.sync_toggle_button(is_recording)

    def handle_record_button_change(self):
        is_recording = self.record_btn.text() == "Stop"  # Check the current state of the record button
        self.update_toggle_button_signal.emit(is_recording)  # Emit the signal to FullDataPage

    def update_checkbox(self, data):
        if data == b'\x41':
            self.connectionCheckbox.setChecked(True)
            self.connectionLabel.setText("Connected")
        elif data == b'\x42':
            self.connectionCheckbox.setChecked(False)
            self.connectionLabel.setText("Not Connected")
    
    def open_data_page(self):
        if not self.full_data_page:
            selected_solution = self.solutionDropdown.currentText()
            self.full_data_page = FullDataPage(self.current_reference_point, selected_solution)
            self.full_data_page.stop_recording_signal.connect(self.handle_stop_recording)
        self.full_data_page.show()

        for entry in self.recorded_data:
            self.full_data_page.update_table(entry[0], entry[1], entry[2], entry[3]) 

    def update_table(self, gain_voltage, phase_voltage):
        water_level = self.calculate_water_level(phase_voltage)
        difference = water_level - self.current_reference_point

        self.timeLastReadingLabel.setText(f"Time of last reading: {datetime.now().strftime('%H:%M:%S')}")
        self.valueLastReadingLabel.setText(f"Value of last reading: {phase_voltage} V")

        self.recorded_data.append((datetime.now().strftime("%H:%M:%S"), water_level, phase_voltage, gain_voltage, difference))
        if self.full_data_page:
            self.full_data_page.update_table(datetime.now().strftime("%H:%M:%S"), water_level, phase_voltage, gain_voltage, difference)
    
    def open_reference_page(self):
        self.referencepoint_btn = ReferencePointPage(self.current_reference_point)
        self.referencepoint_btn.referenceChanged.connect(self.update_reference_label)
        self.referencepoint_btn.show()

    def update_reference_label(self, new_reference):
        self.current_reference_point = int(new_reference)
        self.currentReferenceLabel.setText(f"Current Reference Point: {self.current_reference_point} cm")
        if self.full_data_page:
            self.full_data_page.current_reference_point = self.current_reference_point
            self.full_data_page.update_reference_label()

    def start_serial_thread(self):
        if self.serial_thread is None:
            self.serial_thread = True
            self.serial_thread = SerialThread()
            self.serial_thread.data_received.connect(self.update_table)
            self.thread = threading.Thread(target=self.serial_thread.run)
            self.thread.start()

    def stop_serial_thread(self):
        if self.serial_thread:
            self.serial_thread.stop()
            self.thread.join()
            self.serial_thread = None
            self.thread = None
    
    def check_ftdi_connection(self):
        available_ports = [port.device for port in serial.tools.list_ports.comports()]
        
        if "COM4" in available_ports:
            self.connectionCheckbox.setChecked(True)
            self.connectionLabel.setText("Connected")
        else:
            self.connectionCheckbox.setChecked(False)
            self.connectionLabel.setText("Not Connected")

    def calculate_water_level(self, phase_voltage):
        selected_solution = self.solutionDropdown.currentText()
        if selected_solution == "Tap Solution":
            # if phase_voltage >= 0.9 and phase_voltage <= 1.0:
            #     return 9.0
            # else:
                return WaterLevelCalculator.calculate_tap_water_level(phase_voltage)
        elif selected_solution == "Saline Solution":
            return WaterLevelCalculator.calculate_saline_water_level(phase_voltage)
        elif selected_solution == "Distilled Solution":
            return WaterLevelCalculator.calculate_distilled_water_level(phase_voltage)
        return None

    def update_solution_in_fulldata(self):
        self.selected_solution = self.solutionDropdown.currentText()
        new_solution = self.selected_solution
        print(f"Updating solution to: {new_solution}") 
        self.full_data_page.update_solution_label(new_solution)