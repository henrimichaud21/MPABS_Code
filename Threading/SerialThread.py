import serial
from PyQt5.QtCore import *

# Define port that is being used
Port_Name = "COM4"

# Define the baud rate that is being used
Baud_Rate = 115200

class SerialThread(QObject):
    data_received = pyqtSignal(float, float)

    def __init__(self):
        super().__init__()
        self.port = Port_Name
        self.baudrate = Baud_Rate
        self.running = True
        self.serial_connection = None

    def run(self):
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=1)
            while self.running:
                phase_voltage = None
                gain_voltage = None
                
                if self.serial_connection.in_waiting >= 4:  # 32-bit data
                    data = self.serial_connection.read(4)  # Read 4 bytes (32 bits)
                    gain_value = int.from_bytes(data[:2], "big")  # First 16 bits
                    phase_value = int.from_bytes(data[2:], "big")  # Last 16 bits

                    # Convert to voltage
                    phase_voltage = round((phase_value * 3.3) / 4096, 3)
                    gain_voltage = round((gain_value * 3.3) / 4096, 3)

                    # Emit both values
                    self.data_received.emit(phase_voltage, gain_voltage)

        except serial.SerialException as e:
            print(f"Serial error: {e}")
        finally:
            if self.serial_connection and self.serial_connection.is_open:
                self.serial_connection.close()

    def stop(self):
        self.running = False