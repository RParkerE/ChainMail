import sys
from PyQt6.QtWidgets import QApplication, QDialog
from client.windows.main_window import MainWindow
from client.windows.login_window import LoginWindow
from client.core.client_controller import ClientController

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    controller = ClientController()
    
    while True:
        login = LoginWindow(controller)
        if login.exec() != QDialog.DialogCode.Accepted:
            sys.exit(0)
            
        window = MainWindow(controller)
        window.show()
        result = app.exec()
        
        if not controller.is_logged_in():
            continue
        else:
            sys.exit(result)

if __name__ == "__main__":
    main() 