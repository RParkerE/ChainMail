# ChainMail

ChainMail is a decentralized email client that uses blockchain-inspired concepts for secure, peer-to-peer communication. Built with Python and PyQt6, it provides a familiar email interface while maintaining user privacy and data security.

## Features

- 📧 Decentralized email system
- 🔐 Wallet-based authentication
- 🔒 End-to-end encryption (coming soon)
- 💻 Cross-platform desktop application
- 📁 Local email storage
- 🔄 Real-time email synchronization
- 📝 Draft saving functionality

## Installation

1. Clone the repository: 
```bash
git clone https://github.com/yourusername/chainmail.git
cd chainmail
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Dependencies

- Python 3.8+
- PyQt6
- cryptography
- asyncio

## Usage

1. Start the application:
```bash
python client/main.py
```

2. Create a new account or login with existing credentials

3. Send and receive emails using wallet addresses

4. Use the settings menu to configure your preferences

## Project Structure

chainmail/

├── client/

│ ├── core/

│ │ ├── client_controller.py

│ │ ├── email_manager.py

│ │ ├── settings_manager.py

│ │ └── wallet_manager.py

│ ├── windows/

│ │ ├── compose_window.py

│ │ ├── login_window.py

│ │ ├── main_window.py

│ │ └── settings_window.py

│ ├── utils/

│ │ └── reset.py

│ └── main.py

├── requirements.txt

└── README.md

## Development

### Reset Development Environment

To reset the application state during development:
```bash
python client/utils/reset.py
```

This will remove all wallets, emails, and settings.

### Adding New Features

1. Create feature branch:
```bash
git checkout -b feature-name
```

2. Make changes and test

3. Submit pull request

## Security

- Wallet addresses are generated using RSA-2048
- Passwords are hashed using PBKDF2
- Emails are stored locally in encrypted format (coming soon)
- Private keys never leave the local system

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Future Features

- [ ] Blockchain integration
- [ ] End-to-end encryption
- [ ] Contact management
- [ ] Email attachments
- [ ] Multi-device synchronization
- [ ] Group messaging
- [ ] Email threading
- [ ] Search functionality
- [ ] Spam filtering
- [ ] Email templates

## Troubleshooting

### Common Issues

1. **Login Issues**
   - Ensure wallet address is correct
   - Check password
   - Try resetting application state

2. **Email Delivery**
   - Verify recipient wallet address
   - Check network connection
   - Ensure application is running

3. **UI Issues**
   - Restart application
   - Check PyQt6 installation
   - Update dependencies

### Support

For support, please:
1. Check existing issues
2. Create new issue with detailed description
3. Include error messages and steps to reproduce

## Acknowledgments

- PyQt6 for the UI framework
- Python cryptography library
- Blockchain technology concepts

---
