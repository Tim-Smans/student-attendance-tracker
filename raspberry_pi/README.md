# How to set up a new device
This script allows you to easily set up a new device in the attendance system.

---

## ✅ Prerequisites


Before running the script, ensure the following dependencies are met:

    - Raspberry Pi (At least model 3)
    - The Raspberry Pi AI Camera
    - Latest Raspberry Pi OS




---
## ⚙️ Configuration

Edit the provided `config.yaml` file to customize your setup.

Make sure before running the setup you configured the API key and Room name.
Do **not** use spaces in the configuration values, This will break the setup.

---

## 🛠️ How to Run the Script

Step 1: Make sure you finish the configuration

Step 2: Make the script executable
`
chmod +x setup.sh
`

Step 3: Run the script
`
./setup_mlops.sh
`

While running the script:
1. It will create a virtual environment using python venv
2. And will install all global packages and the libraries inside the virtual environment
3. Runs the python script that adds the device to the database

Step 3: Finish The installation
`
Reboot the device to activate the scanning
`