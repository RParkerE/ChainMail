import os
import shutil
from pathlib import Path

def reset_chainmail():
    """Reset the ChainMail application by removing all data."""
    # Get the .chainmail directory path
    chainmail_dir = os.path.join(str(Path.home()), '.chainmail')
    
    try:
        # Remove the entire .chainmail directory
        if os.path.exists(chainmail_dir):
            shutil.rmtree(chainmail_dir)
            print(f"Successfully reset ChainMail data at: {chainmail_dir}")
        else:
            print("No ChainMail data found to reset.")
    except Exception as e:
        print(f"Error resetting ChainMail: {e}")

if __name__ == "__main__":
    # Ask for confirmation
    response = input("This will delete all wallets and emails. Are you sure? (y/N): ")
    if response.lower() == 'y':
        reset_chainmail()
    else:
        print("Reset cancelled.") 