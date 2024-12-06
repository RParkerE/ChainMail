from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QTreeWidget, QTreeWidgetItem, QSplitter,
                           QTextEdit, QLabel, QLineEdit)
from PyQt6.QtCore import Qt
from client.windows.compose_window import ComposeWindow
from client.windows.settings_window import SettingsWindow

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.controller.email_manager.emails_updated.connect(self.refresh_emails)
        self.init_ui()
        self.refresh_emails()

    def init_ui(self):
        self.setWindowTitle('Blockchain Email Client')
        self.setGeometry(100, 100, 1200, 800)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)

        # Left panel (folders and navigation)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Wallet address display
        self.wallet_label = QLabel("Wallet Address:")
        self.wallet_address = QLineEdit()
        self.wallet_address.setReadOnly(True)
        left_layout.addWidget(self.wallet_label)
        left_layout.addWidget(self.wallet_address)

        # Folder tree
        self.folder_tree = QTreeWidget()
        self.folder_tree.setHeaderLabel("Folders")
        self.setup_folders()
        left_layout.addWidget(self.folder_tree)

        # Buttons
        compose_btn = QPushButton("Compose")
        compose_btn.clicked.connect(self.show_compose_window)
        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(self.show_settings)
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.logout)
        left_layout.addWidget(compose_btn)
        left_layout.addWidget(settings_btn)
        left_layout.addWidget(logout_btn)

        # Right panel (email list and preview)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Email list
        self.email_list = QTreeWidget()
        self.email_list.setHeaderLabels(["Subject", "From", "Date"])
        self.email_list.itemClicked.connect(self.show_email)
        
        # Email preview
        self.email_preview = QTextEdit()
        self.email_preview.setReadOnly(True)

        right_layout.addWidget(self.email_list)
        right_layout.addWidget(self.email_preview)

        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)

        # Set initial splitter sizes
        splitter.setSizes([300, 900])

    def setup_folders(self):
        folders = [
            "Inbox",
            "Sent",
            "Drafts",
            "Archive",
            "Spam",
            "Trash"
        ]
        for folder in folders:
            item = QTreeWidgetItem(self.folder_tree)
            item.setText(0, folder)
        self.folder_tree.itemClicked.connect(self.load_folder)

    def show_compose_window(self):
        self.compose_window = ComposeWindow(self.controller)
        self.compose_window.show()

    def show_settings(self):
        self.settings_window = SettingsWindow(self.controller)
        self.settings_window.show()

    def load_folder(self, item):
        folder_name = item.text(0)
        emails = self.controller.get_emails(folder_name)
        self.email_list.clear()
        for email in emails:
            item = QTreeWidgetItem(self.email_list)
            item.setText(0, email['subject'])
            item.setText(1, email['from'])
            item.setText(2, email['date'])
            item.setData(0, Qt.ItemDataRole.UserRole, email)

    def show_email(self, item):
        email_data = item.data(0, Qt.ItemDataRole.UserRole)
        self.email_preview.setHtml(email_data['content'])

    def refresh_emails(self):
        """Refresh the email list when new emails arrive."""
        current_folder = self.folder_tree.currentItem()
        if current_folder:
            self.load_folder(current_folder)

    def logout(self):
        self.controller.logout()
        self.close()
        from client.windows.login_window import LoginWindow
        login = LoginWindow(self.controller)
        if login.exec() == QDialog.DialogCode.Accepted:
            self.show()
        else:
            self.close()
    