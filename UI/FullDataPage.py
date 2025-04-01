import sys
import csv
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QDir
from UI.ReferencePointPage import ReferencePointPage
from datetime import datetime
from PyQt5.QtCore import pyqtSignal

class FullDataPage(QWidget):
    stop_recording_signal = pyqtSignal(bool)
    def __init__(self, reference_point, selected_solution):
        super().__init__()
        self.setGeometry(1000, 100, 800, 700)
        self.setWindowTitle("Microstrip Patch Antenna Full Data Page")

        font = QFont()
        font.setPointSize(9)
        font.setBold(True)

        self.table = QTableWidget(self)
        self.table.setRowCount(0)
        self.table.setColumnCount(5)
        self.table.setFixedSize(700, 700)
        self.table.move(50,75)
        self.table.setHorizontalHeaderLabels(["Time","Water\nLevel (cm)", "Phase (V)", "Gain (V)", "Difference From\nRef. Point (cm)"])
        self.table.horizontalHeader().setFont(font)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 125)
        self.table.setColumnWidth(3, 125)
        self.table.setColumnWidth(4, 250)


        # Add Export to CSV Button
        self.exportData_btn = QPushButton("Export Data", self)
        self.exportData_btn.setStyleSheet("font-size: 16px")
        self.exportData_btn.setFixedSize(125, 50)
        self.exportData_btn.move(525, 10)
        self.exportData_btn.clicked.connect(self.export_Table)

        # Add Clear Data Button
        self.clearData_btn = QPushButton("Clear Data", self)
        self.clearData_btn.setStyleSheet("font-size: 16px")
        self.clearData_btn.setFixedSize(125, 50)
        self.clearData_btn.move(400, 10)
        self.clearData_btn.clicked.connect(self.clear_table)

        # Stop/Resume Recording Button
        self.toggleRecording_btn = QPushButton("Stop", self)
        self.toggleRecording_btn.setStyleSheet("font-size: 16px")
        self.toggleRecording_btn.setFixedSize(125, 50)
        self.toggleRecording_btn.move(275, 10)
        self.toggleRecording_btn.clicked.connect(self.toggle_recording)

        self.is_recording = True

        # Reference Point Label
        self.current_reference_point = "0" 
        self.currentReferenceLabel = QLabel(f"Reference Point: {self.current_reference_point} cm", self)
        self.currentReferenceLabel.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.currentReferenceLabel.setFixedSize(275,30)
        self.currentReferenceLabel.move(50,10)

        # Solution Label
        self.current_solution = selected_solution 
        self.currentSolutionLabel = QLabel(f"Solution: {self.current_solution}", self)
        self.currentSolutionLabel.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.currentSolutionLabel.setFixedSize(500,30)
        self.currentSolutionLabel.move(50,40)

    def update_table(self, current_time, water_level, phase_voltage, gain_voltage, difference):
        current_time = datetime.now().strftime("%H:%M:%S")
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)

        self.table.setItem(row_count, 0, QTableWidgetItem(current_time))
        self.table.setItem(row_count, 1, QTableWidgetItem(str(water_level)))
        self.table.setItem(row_count, 2, QTableWidgetItem(str(phase_voltage))) 
        self.table.setItem(row_count, 3, QTableWidgetItem(str(gain_voltage)))
        self.table.setItem(row_count, 4, QTableWidgetItem(str(difference))) 
        self.table.scrollToBottom()

    def open_reference_page(self):
        self.referencepoint_btn = ReferencePointPage()
        self.referencepoint_btn.show()

    def update_reference_label(self):
        self.currentReferenceLabel.setText(f"Reference Point: {self.current_reference_point} cm")

    def clear_table(self):
        self.table.setRowCount(0)

    def toggle_recording(self):
        if self.is_recording:
            self.toggleRecording_btn.setText("Resume")
            self.stop_recording_signal.emit(False)
        else:
            self.toggleRecording_btn.setText("Stop") 
            self.stop_recording_signal.emit(True)
        self.stop_recording_signal.emit(self.is_recording)
    
    def update_toggle_recording_state(self, is_recording):
        if is_recording:
            self.toggleRecording_btn.setText("Stop")
        else:
            self.toggleRecording_btn.setText("Resume")

    def sync_toggle_button(self, is_recording):
        self.is_recording = is_recording
        self.toggleRecording_btn.setChecked(is_recording)
        self.toggleRecording_btn.setText("Stop" if is_recording else "Resume")

    def update_solution_label(self, new_solution):
        print(f"Updating label to: {new_solution}") 
        self.current_solution = new_solution
        self.currentSolutionLabel.setText(f"Solution: {self.current_solution}")

    def export_Table(self):
        path, _= QFileDialog.getSaveFileName(self, 'Save File', QDir.homePath() + "/export.csv", "CSV Files(*.csv *.txt)")
        if path:
            with open(path, 'w') as stream:
                print("saving", path)
                writer = csv.writer(stream, dialect='excel', delimiter= ',')
                headers = []

                for column in range(self.table.columnCount()):
                    header = self.table.horizontalHeaderItem(column)
                    if header:
                        headers.append(header.text())
                    else:
                        headers.append(f"Column {column}")
                writer.writerow(headers)

                for row in range(self.table.rowCount()):
                    rowData = []
                    for column in range(self.table.columnCount()):
                        item = self.table.item(row, column)
                        if item is not None:
                            rowData.append(item.text())
                        else:
                            rowData.append('')
                    writer.writerow(rowData)