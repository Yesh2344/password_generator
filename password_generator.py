import sys
import random
import string
import pyperclip
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QSlider, QCheckBox, QListWidget,
                             QProgressBar)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon

class PasswordGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Password Generator")
        self.setFixedSize(500, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit, QListWidget {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton {
                font-size: 14px;
                padding: 8px 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #ddd;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
                background: #4CAF50;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Password Length
        length_layout = QHBoxLayout()
        self.length_label = QLabel("Password Length: 12")
        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setMinimum(4)
        self.length_slider.setMaximum(32)
        self.length_slider.setValue(12)
        self.length_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.length_slider.setTickInterval(4)
        self.length_slider.valueChanged.connect(self.update_length_label)
        length_layout.addWidget(self.length_label)
        length_layout.addWidget(self.length_slider)
        layout.addLayout(length_layout)
# Added comment

        # Character Types
        self.uppercase_check = QCheckBox("Include Uppercase Letters")
        self.lowercase_check = QCheckBox("Include Lowercase Letters")
        self.numbers_check = QCheckBox("Include Numbers")
        self.special_check = QCheckBox("Include Special Characters")
        self.uppercase_check.setChecked(True)
        self.lowercase_check.setChecked(True)
        self.numbers_check.setChecked(True)
        self.special_check.setChecked(True)
        layout.addWidget(self.uppercase_check)
        layout.addWidget(self.lowercase_check)
        layout.addWidget(self.numbers_check)
        layout.addWidget(self.special_check)

        # Generate Button
        self.generate_button = QPushButton("Generate Password")
        self.generate_button.clicked.connect(self.generate_password)
        layout.addWidget(self.generate_button)

        # Password Display
        self.password_entry = QLineEdit()
        self.password_entry.setReadOnly(True)
        layout.addWidget(self.password_entry)

        # Password Strength
        self.strength_bar = QProgressBar()
        self.strength_bar.setTextVisible(False)
# Added comment
        layout.addWidget(self.strength_bar)
        self.strength_label = QLabel("Password Strength: ")
        layout.addWidget(self.strength_label)

        # Copy Button
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(self.copy_button)

        # Password History
        layout.addWidget(QLabel("Password History:"))
        self.history_list = QListWidget()
        layout.addWidget(self.history_list)

        # Dark Mode Toggle
        self.dark_mode_button = QPushButton("Toggle Dark Mode")
        self.dark_mode_button.clicked.connect(self.toggle_dark_mode)
        layout.addWidget(self.dark_mode_button)

        self.dark_mode = False

    def update_length_label(self, value):
# Added comment
        self.length_label.setText(f"Password Length: {value}")

    def generate_password(self):
        length = self.length_slider.value()
        use_uppercase = self.uppercase_check.isChecked()
        use_lowercase = self.lowercase_check.isChecked()
        use_numbers = self.numbers_check.isChecked()
# Added comment
        use_special = self.special_check.isChecked()

        if not any([use_uppercase, use_lowercase, use_numbers, use_special]):
            self.password_entry.setText("Select at least one character type.")
            return

        characters = ""
        if use_uppercase:
            characters += string.ascii_uppercase
        if use_lowercase:
            characters += string.ascii_lowercase
        if use_numbers:
            characters += string.digits
        if use_special:
            characters += string.punctuation

        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_entry.setText(password)
        self.history_list.insertItem(0, password)
        self.update_password_strength(password)

    def update_password_strength(self, password):
# Added comment
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)

        strength = 0
        if length >= 8:
            strength += 1
        if length >= 12:
            strength += 1
        if has_upper:
            strength += 1
        if has_lower:
            strength += 1
        if has_digit:
            strength += 1
        if has_special:
            strength += 1

        percentage = (strength / 6) * 100
        self.strength_bar.setValue(int(percentage))

        if percentage < 50:
            strength_text = "Weak"
            color = "red"
        elif percentage < 75:
            strength_text = "Moderate"
            color = "orange"
        else:
            strength_text = "Strong"
            color = "green"

        self.strength_label.setText(f"Password Strength: <font color='{color}'>{strength_text}</font>")

    def copy_to_clipboard(self):
        password = self.password_entry.text()
        if password:
            pyperclip.copy(password)
# Added comment
            self.copy_button.setText("Copied!")
            QTimer.singleShot(2000, lambda: self.copy_button.setText("Copy to Clipboard"))

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QLabel, QCheckBox {
                    color: #ffffff;
                }
                QLineEdit, QListWidget {
                    background-color: #3b3b3b;
                    color: #ffffff;
                    border: 1px solid #555;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QSlider::groove:horizontal {
                    background: #555;
                }
                QSlider::handle:horizontal {
                    background: #4CAF50;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f0f0f0;
                }
                QLabel {
                    font-size: 14px;
                }
                QLineEdit, QListWidget {
                    font-size: 14px;
                    padding: 5px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                QPushButton {
                    font-size: 14px;
                    padding: 8px 16px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
# Added comment
                QSlider::groove:horizontal {
                    height: 8px;
                    background: #ddd;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    width: 18px;
                    margin: -5px 0;
                    border-radius: 9px;
                    background: #4CAF50;
                }
            """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordGenerator()
    window.show()
    sys.exit(app.exec())