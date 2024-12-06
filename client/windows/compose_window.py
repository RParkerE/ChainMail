from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLineEdit,
                           QTextEdit, QPushButton, QLabel)
from PyQt6.QtCore import Qt

class ComposeWindow(QDialog):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Compose Email')
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()

        # To field
        to_layout = QHBoxLayout()
        to_label = QLabel("To:")
        self.to_input = QLineEdit()
        to_layout.addWidget(to_label)
        to_layout.addWidget(self.to_input)
        layout.addLayout(to_layout)

        # Subject field
        subject_layout = QHBoxLayout()
        subject_label = QLabel("Subject:")
        self.subject_input = QLineEdit()
        subject_layout.addWidget(subject_label)
        subject_layout.addWidget(self.subject_input)
        layout.addLayout(subject_layout)

        # Message body
        self.message_input = QTextEdit()
        layout.addWidget(self.message_input)

        # Buttons
        button_layout = QHBoxLayout()
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_email)
        save_draft_button = QPushButton("Save Draft")
        save_draft_button.clicked.connect(self.save_draft)
        button_layout.addWidget(send_button)
        button_layout.addWidget(save_draft_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def send_email(self):
        email_data = {
            'to': self.to_input.text(),
            'subject': self.subject_input.text(),
            'content': self.message_input.toPlainText()
        }
        self.controller.send_email(email_data)
        self.accept()

    def save_draft(self):
        email_data = {
            'to': self.to_input.text(),
            'subject': self.subject_input.text(),
            'content': self.message_input.toPlainText()
        }
        self.controller.save_draft(email_data)
        self.accept() 