set -e

CONFIG_FILE="config.yaml"

if ! command -v yq &> /dev/null
then
    echo "yq not found, installing temporarily..."

    ARCH=$(uname -m)

    if [[ "$ARCH" == "aarch64" ]]; then
        echo "ARM64 architecture detected"
        wget -qO yq "https://github.com/mikefarah/yq/releases/latest/download/yq_linux_arm64"
    elif [[ "$ARCH" == "armv7l" ]]; then
        echo "ARMv7 architecture detected"
        wget -qO yq "https://github.com/mikefarah/yq/releases/latest/download/yq_linux_arm"
    else
        echo "Unsupported architecture: $ARCH"
        exit 1
    fi

    chmod +x yq
fi

ROOM_NAME=$(./yq  '.room_name' $CONFIG_FILE)
API_KEY=$(./yq '.api_key' $CONFIG_FILE)
DEVICE_IDENTIFIER=$(awk '/Serial/ {print $3}' /proc/cpuinfo)


sudo apt update
sudo apt install libzbar0 tesseract-ocr

python3 -m venv .venv --system-site-packages
source .venv/bin/activate

pip install -r requirements.txt

python3 scripts/setup.py $ROOM_NAME $DEVICE_IDENTIFIER $API_KEY

# Create .env file
tee .env > /dev/null <<EOF
API_KEY=$API_KEY
EOF

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

# Reload systemd to pick up the new service
sudo systemctl daemon-reload

# Enable service to start at boot
sudo systemctl enable student-attendance.service

# Start the new service immediately
sudo systemctl start student-attendance.service

echo "Finished setting up student attendance tracker on this device!"