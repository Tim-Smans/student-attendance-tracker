#!/bin/bash

echo ""
echo "First Boot Configuration Raspberry Pi"

read -p "New hostname (ex: pi-roomname) (should be unique): " NEW_HOSTNAME
sudo hostnamectl set-hostname "$NEW_HOSTNAME"
echo "$NEW_HOSTNAME" | sudo tee /etc/hostname
sudo sed -i "s/127.0.1.1.*/127.0.1.1\t$NEW_HOSTNAME/" /etc/hosts
echo "Hostname set"

read -p "Setup? (y/N): " WIFI_CHOICE
if [[ "$WIFI_CHOICE" == "y" ]]; then
  read -p "SSID: " SSID
  read -s -p "Password: " PASSWORD
  echo
  sudo tee /etc/wpa_supplicant/wpa_supplicant.conf > /dev/null <<EOF
country=FI
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="$SSID"
    psk="$PASSWORD"
}
EOF
  sudo chmod 600 /etc/wpa_supplicant/wpa_supplicant.conf
  echo "Wifi has been set up"
fi

read -p "Room name (ex: C120): " ROOM_NAME
read -p "API KEY: " API_KEY
DEVICE_IDENTIFIER=$(awk '/Serial/ {print $3}' /proc/cpuinfo)

echo "Installing apt packages..."

sudo apt update
sudo apt install libzbar0 tesseract-ocr python3-smbus

sudo sed -i '$ai2c_arm=on' /boot/config.txt

# Going to project repository directory
cd /home/metro/student-attendance-tracker/raspberry_pi
git pull

python3 -m venv .venv --system-site-packages
source .venv/bin/activate

# Installing Python libraries
echo "Installing Python libraries..."
pip install -r requirements.txt

# Add room to database
python3 scripts/setup.py $ROOM_NAME $DEVICE_IDENTIFIER $API_KEY

# Create env
tee .env > /dev/null <<EOF
API_KEY=$API_KEY
EOF

chmod +x /home/metro/student-attendance-tracker/raspberry_pi/scripts/startup.sh

# Create the systemd service
USER_HOME="/home/$(whoami)"

sudo tee /etc/systemd/system/student-attendance.service > /dev/null <<EOF
[Unit]
Description=Start Student Attendance Tracker
After=network.target

[Service]
ExecStart=$USER_HOME/student-attendance-tracker/raspberry_pi/scripts/startup.sh
Restart=always
User=$(whoami)
WorkingDirectory=$USER_HOME/student-attendance-tracker/raspberry_pi
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

# Create ping systemd service
sudo tee /etc/systemd/system/pi-pinger.service > /dev/null <<EOF
[Unit]
Description=Ping backend to report Pi status

[Service]
Type=oneshot
ExecStart=$USER_HOME/student-attendance-tracker/raspberry_pi/.venv/bin/python $USER_HOME/student-attendance-tracker/raspberry_pi/scripts/ping_backend.py
User=$(whoami)
WorkingDirectory=$USER_HOME/student-attendance-tracker/raspberry_pi
EOF

# Create ping systemd timer (runs every minute)
sudo tee /etc/systemd/system/pi-pinger.timer > /dev/null <<EOF
[Unit]
Description=Run Pi Pinger every minute

[Timer]
OnBootSec=30s
OnUnitActiveSec=60s
Unit=pi-pinger.service

[Install]
WantedBy=timers.target
EOF

# Reload systemd and enable services
sudo systemctl daemon-reload
sudo systemctl enable student-attendance.service
sudo systemctl start student-attendance.service

sudo systemctl enable pi-pinger.timer
sudo systemctl start pi-pinger.timer



sed -i '/firstboot.sh/d' ~/.bashrc
rm -- "$0"
sudo systemctl disable firstboot.service
sudo rm /etc/systemd/system/firstboot.service

echo "Finished setting up student attendance tracker on this device! Reboot recomended: sudo reboot"
