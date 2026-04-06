import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QTextEdit, QFileDialog
)
from PyQt6.QtCore import QProcess, Qt

class BleuIOUpdaterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BleuIO Firmware Updater")
        self.setMinimumSize(600, 400)
        self.resize(700, 500)

        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.finished.connect(self.process_finished)

        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Title
        title_label = QLabel("BleuIO Firmware Updater")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # File Selection Frame
        file_layout = QHBoxLayout()
        self.file_entry = QLineEdit()
        self.file_entry.setPlaceholderText("Select firmware (.img) file...")
        self.file_entry.setReadOnly(True)
        file_layout.addWidget(self.file_entry)

        self.browse_btn = QPushButton("Browse")
        self.browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(self.browse_btn)

        layout.addLayout(file_layout)

        # Options Frame
        options_layout = QHBoxLayout()
        self.debug_check = QCheckBox("Enable Debug Output (-dbg)")
        options_layout.addWidget(self.debug_check)
        options_layout.addStretch()
        layout.addLayout(options_layout)

        # Buttons Layout
        button_layout = QHBoxLayout()

        # Update Button
        self.update_btn = QPushButton("Update Firmware")
        self.update_btn.setMinimumHeight(40)
        self.update_btn.setStyleSheet("font-weight: bold;")
        self.update_btn.clicked.connect(self.start_update)
        button_layout.addWidget(self.update_btn)

        # Stop Button
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setMinimumHeight(40)
        self.stop_btn.setStyleSheet("font-weight: bold; color: red;")
        self.stop_btn.clicked.connect(self.stop_update)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)

        layout.addLayout(button_layout)

        # Console Output Text
        self.console_text = QTextEdit()
        self.console_text.setReadOnly(True)
        self.console_text.setFontFamily("Courier")
        layout.addWidget(self.console_text)

    def browse_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Firmware Image",
            "",
            "Image Files (*.img);;All Files (*)"
        )
        if filename:
            self.file_entry.setText(filename)

    def append_console(self, text):
        self.console_text.moveCursor(self.console_text.textCursor().MoveOperation.End)
        self.console_text.insertPlainText(text)
        self.console_text.verticalScrollBar().setValue(
            self.console_text.verticalScrollBar().maximum()
        )

    def start_update(self):
        firmware_path = self.file_entry.text()
        if not firmware_path or not os.path.isfile(firmware_path):
            self.append_console("Error: Please select a valid firmware file.\n")
            return

        self.update_btn.setEnabled(False)
        self.browse_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.console_text.clear()

        self.append_console(f"Starting update with {os.path.basename(firmware_path)}...\n" + "-"*50 + "\n")

        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bleuio_fw_updater.py')
        
        args = ["-u", script_path, firmware_path]
        if self.debug_check.isChecked():
            args.append("--debug")

        # Start the subprocess
        self.process.start(sys.executable, args)

    def handle_stdout(self):
        data = self.process.readAllStandardOutput().data().decode('utf-8', errors='replace')
        self.append_console(data)

        # Watch for the interactive prompt from the updater script
        text_content = self.console_text.toPlainText()
        if "Run again?" in text_content or "Try again?" in text_content:
            if ">>" in text_content.splitlines()[-1]:
                if self.process.state() == QProcess.ProcessState.Running:
                    self.process.write(b"n\n")

    def stop_update(self):
        if self.process.state() == QProcess.ProcessState.Running:
            self.append_console("\n[User Sent Stop/Break Signal]\n")
            # Sending interrupt (SIGINT/SIGTERM) to break the run process
            try:
                import signal
                os.kill(self.process.processId(), signal.SIGINT)
            except Exception:
                self.process.terminate()

    def process_finished(self):
        self.append_console("\n[Update Process Finished]\n")
        self.update_btn.setEnabled(True)
        self.browse_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Optional styling to make it darker/modern natively
    app.setStyle('Fusion')

    window = BleuIOUpdaterGUI()
    window.show()
    sys.exit(app.exec())
