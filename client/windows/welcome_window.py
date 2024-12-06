from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QLineEdit, QWidget, QProgressBar)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap

class WelcomeWindow(QDialog):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Welcome to ChainMail')
        self.setGeometry(100, 100, 600, 400)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        
        layout = QVBoxLayout()
        
        # Welcome message
        welcome_label = QLabel("Welcome to ChainMail")
        welcome_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)
        
        # Description
        desc_label = QLabel(
            "ChainMail is a decentralized email system that uses blockchain "
            "technology to ensure your emails are private, secure, and encrypted."
        )
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc_label)
        
        # Create new wallet section
        self.create_wallet_widget(layout)
        
        # Import existing wallet section
        self.import_wallet_widget(layout)
        
        self.setLayout(layout)
        
    def create_wallet_widget(self, parent_layout):
        group = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel("Create New Wallet")
        label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        layout.addWidget(label)
        
        desc = QLabel(
            "Create a new blockchain email address. This will be your "
            "unique identifier for sending and receiving emails."
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        create_btn = QPushButton("Create New Wallet")
        create_btn.setMinimumHeight(40)
        create_btn.clicked.connect(self.create_new_wallet)
        layout.addWidget(create_btn)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
        
    def import_wallet_widget(self, parent_layout):
        group = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel("Import Existing Wallet")
        label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        layout.addWidget(label)
        
        desc = QLabel(
            "Already have a wallet? Import your existing wallet to access "
            "your blockchain email account."
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        import_btn = QPushButton("Import Wallet")
        import_btn.setMinimumHeight(40)
        import_btn.clicked.connect(self.import_wallet)
        layout.addWidget(import_btn)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
        
    def create_new_wallet(self):
        self.show_progress_dialog("Creating New Wallet", "Generating secure keys...")
        # Create wallet in a non-blocking way
        QTimer.singleShot(100, self._create_wallet_process)
        
    def _create_wallet_process(self):
        try:
            self.controller.create_new_wallet()
            self.progress_dialog.setValue(100)
            self.progress_dialog.setLabelText("Wallet created successfully!")
            QTimer.singleShot(1000, self.accept)
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Failed to create wallet: {str(e)}")
            self.progress_dialog.close()
            
    def import_wallet(self):
        from PyQt6.QtWidgets import QFileDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Import Wallet File",
            "",
            "Wallet Files (*.json);;All Files (*)"
        )
        
        if file_name:
            try:
                self.controller.import_wallet(file_name)
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import wallet: {str(e)}")
                
    def show_progress_dialog(self, title, text):
        from PyQt6.QtWidgets import QProgressDialog
        self.progress_dialog = QProgressDialog(text, None, 0, 100, self)
        self.progress_dialog.setWindowTitle(title)
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.setAutoClose(False)
        self.progress_dialog.setAutoReset(False)
        self.progress_dialog.setValue(0)
        self.progress_dialog.show() 