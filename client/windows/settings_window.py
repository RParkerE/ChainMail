from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLineEdit,
                           QPushButton, QLabel, QGroupBox, QFormLayout,
                           QCheckBox, QSpinBox)
from PyQt6.QtCore import Qt

class SettingsWindow(QDialog):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        self.setWindowTitle('Settings')
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()

        # Wallet Settings
        wallet_group = QGroupBox("Wallet Settings")
        wallet_layout = QFormLayout()
        
        self.wallet_address = QLineEdit()
        self.wallet_address.setReadOnly(True)
        wallet_layout.addRow("Wallet Address:", self.wallet_address)
        
        generate_wallet_btn = QPushButton("Generate New Wallet")
        generate_wallet_btn.clicked.connect(self.generate_new_wallet)
        wallet_layout.addRow("", generate_wallet_btn)
        
        wallet_group.setLayout(wallet_layout)
        layout.addWidget(wallet_group)

        # Network Settings
        network_group = QGroupBox("Network Settings")
        network_layout = QFormLayout()
        
        self.node_address = QLineEdit()
        network_layout.addRow("Node Address:", self.node_address)
        
        self.node_port = QSpinBox()
        self.node_port.setRange(1, 65535)
        self.node_port.setValue(8000)
        network_layout.addRow("Node Port:", self.node_port)
        
        network_group.setLayout(network_layout)
        layout.addWidget(network_group)

        # Email Settings
        email_group = QGroupBox("Email Settings")
        email_layout = QFormLayout()
        
        self.auto_sync = QCheckBox()
        email_layout.addRow("Auto Sync:", self.auto_sync)
        
        self.sync_interval = QSpinBox()
        self.sync_interval.setRange(1, 60)
        self.sync_interval.setValue(5)
        email_layout.addRow("Sync Interval (minutes):", self.sync_interval)
        
        self.encryption_enabled = QCheckBox()
        self.encryption_enabled.setChecked(True)
        self.encryption_enabled.setEnabled(False)  # Always enabled for blockchain emails
        email_layout.addRow("End-to-End Encryption:", self.encryption_enabled)
        
        email_group.setLayout(email_layout)
        layout.addWidget(email_group)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_settings(self):
        settings = self.controller.settings_manager.load_settings()
        
        # Load wallet settings
        self.wallet_address.setText(settings.get('wallet_address', ''))
        
        # Load network settings
        self.node_address.setText(settings.get('node_address', 'localhost'))
        self.node_port.setValue(settings.get('node_port', 8000))
        
        # Load email settings
        self.auto_sync.setChecked(settings.get('auto_sync', True))
        self.sync_interval.setValue(settings.get('sync_interval', 5))

    def save_settings(self):
        settings = {
            'wallet_address': self.wallet_address.text(),
            'node_address': self.node_address.text(),
            'node_port': self.node_port.value(),
            'auto_sync': self.auto_sync.isChecked(),
            'sync_interval': self.sync_interval.value(),
            'encryption_enabled': True  # Always enabled
        }
        
        self.controller.update_settings(settings)
        self.accept()

    def generate_new_wallet(self):
        if self.show_warning_dialog():
            self.controller.create_new_wallet()
            self.wallet_address.setText(self.controller.get_wallet_address())

    def show_warning_dialog(self) -> bool:
        from PyQt6.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText("Are you sure you want to generate a new wallet?")
        msg.setInformativeText("This will create a new blockchain email address. "
                             "You will not be able to access emails sent to your old address.")
        msg.setWindowTitle("Warning")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        return msg.exec() == QMessageBox.StandardButton.Yes 