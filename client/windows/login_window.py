from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QLineEdit, QMessageBox, QStackedWidget,
                           QWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class LoginWindow(QDialog):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle('ChainMail Login')
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()

    def init_ui(self):
        self.stacked_widget = QStackedWidget()
        layout = QVBoxLayout()
        
        # Login page
        login_widget = self.create_login_widget()
        self.stacked_widget.addWidget(login_widget)
        
        # Create account page
        create_account_widget = self.create_account_widget()
        self.stacked_widget.addWidget(create_account_widget)
        
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    def create_login_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Login to ChainMail")
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Wallet address input
        self.wallet_input = QLineEdit()
        self.wallet_input.setPlaceholderText("Enter Wallet Address")
        layout.addWidget(self.wallet_input)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Login button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)

        # Create account link
        create_account_btn = QPushButton("Create New Account")
        create_account_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(create_account_btn)

        widget.setLayout(layout)
        return widget

    def create_account_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Create New Account")
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Password input
        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("Enter Password")
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.new_password)

        # Confirm password
        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirm Password")
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_password)

        # Create account button
        create_btn = QPushButton("Create Account")
        create_btn.clicked.connect(self.create_account)
        layout.addWidget(create_btn)

        # Back to login
        back_btn = QPushButton("Back to Login")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn)

        widget.setLayout(layout)
        return widget

    def login(self):
        wallet_address = self.wallet_input.text()
        password = self.password_input.text()
        
        if self.controller.login(wallet_address, password):
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", 
                              "Invalid wallet address or password")

    def create_account(self):
        if self.new_password.text() != self.confirm_password.text():
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return

        try:
            wallet_address = self.controller.create_account(self.new_password.text())
            QMessageBox.information(self, "Success", 
                                  f"Account created successfully!\nYour wallet address is:\n{wallet_address}\n\nPlease save this address!")
            self.wallet_input.setText(wallet_address)
            self.stacked_widget.setCurrentIndex(0)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create account: {str(e)}") 