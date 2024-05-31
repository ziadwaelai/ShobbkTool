import sys
import os
from threading import Thread
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QLabel, QCheckBox, QPushButton, QTextEdit, QVBoxLayout, QScrollArea, QWidget
from PIL import Image,ImageQt
import addFolders as af
import removeBackground as rb
import addBackground as ab
import resize as ri
import download as di
import checkAndEditFormat as cf

class ShobbakTool(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.input_folder = "input"
        self.output_folder = "output"
        self.init_ui()

    def init_ui(self):

        self.setGeometry(100, 100, 700, 1000) # Set the window size
        self.setWindowTitle("Shobbak Tool")
        self.setFixedSize(700, 1000)  # Adjust size to match the provided image

        # icon
        icon_path = self.resource_path("assets/icon.png")
        app_icon = QtGui.QIcon(icon_path)
        self.setWindowIcon(app_icon)
        layout = QVBoxLayout()

        # Add company logo
        logo_path = self.resource_path("assets/logo.png")
        try:
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((400, 100), Image.LANCZOS)
            logo_photo = QtGui.QPixmap.fromImage(QtGui.QImage(logo_path)).scaled(450, 100)
            logo_label = QLabel(self)
            logo_label.setPixmap(logo_photo)
            # Center the logo
            logo_container = QtWidgets.QHBoxLayout()
            logo_container.addStretch(1)
            logo_container.addWidget(logo_label)
            logo_container.addStretch(1)
            layout.addLayout(logo_container)
        except Exception as e:
            print(f"Error loading image: {e}")

        # Options
        self.options = {
            "Download Images": QCheckBox("Download Images"),
            "Compress Images": QCheckBox("Compress Images"),
            "Remove Background": QCheckBox("Remove Background"),
            "Add Background": QCheckBox("Add Background"),
            "Resize": QCheckBox("Resize"),
        }
        self.options["Compress Images"].setChecked(True)
        self.options["Resize"].setChecked(True)

        for option in self.options.values():
            option.setStyleSheet("QCheckBox::indicator:checked {background-color: #10B981; border: 1px solid #10B981;} QCheckBox::indicator:unchecked {background-color: #FFFFFF; border: 1px solid #10B981;} QCheckBox {color: #000000; font-size: 15px;}")
            layout.addWidget(option)
        # Logs
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.logs)
        layout.addWidget(scroll_area)

        # Run Button
        self.run_button = QPushButton("Run")
        self.run_button.setStyleSheet("QPushButton {background-color: #10B981; color: white; padding:10px 5px; border-radius: 10px; height: 40px; font-size: 25px; font-weight: bold;} QPushButton:hover {background-color: #0E9568;}")
        self.run_button.clicked.connect(self.run_tool)
        layout.addWidget(self.run_button)

        self.setLayout(layout)

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def print_logs(self, text):
        self.logs.append(text)
        self.logs.verticalScrollBar().setValue(self.logs.verticalScrollBar().maximum())

    def run_tool(self):
        thread = Thread(target=self.run_tool_thread)
        thread.start()

    def run_tool_thread(self):
        af.delete_folder(self.output_folder)
        af.folder_creation_helpe("input")
        af.folder_creation_helpe("output")
        self.print_logs("Starting...\n")
        self.print_logs("Checking and Editing Format...\n")
        cf.convert_images_to_jpg("input", "output")
        self.print_logs("-------------------------------------------\n")

        if self.options["Download Images"].isChecked():
            self.print_logs("Downloading Images...\n")
            di.download_images("input", "input", self.print_logs)
            self.print_logs("-------------------------------------------\n")
            cf.convert_images_to_jpg("input", "output")

        if self.options["Remove Background"].isChecked():
            self.print_logs("Removing Background...\n")
            rb.remove_background("output", "output", self.print_logs)
            self.print_logs("-------------------------------------------\n")

        if self.options["Add Background"].isChecked():
            self.print_logs("Adding Background...\n")
            ab.add_background("output", "output", self.print_logs)
            self.print_logs("-------------------------------------------\n")

        if self.options["Compress Images"].isChecked():
            self.print_logs("Checking and Editing Format...\n")
            cf.convert_images_to_jpg("output", "output", self.print_logs)
            self.print_logs("Compressing Images...\n")
            cf.compress_images("output", "output", self.print_logs)
            self.print_logs("-------------------------------------------\n")

        if self.options["Resize"].isChecked():
            self.print_logs("Resizing Images...\n")
            ri.resize_images_in_folder("output", "output", self.print_logs)
            self.print_logs("-------------------------------------------\n")

        self.print_logs("Done.\n")
