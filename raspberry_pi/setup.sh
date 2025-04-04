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
DEVICE_IDENTIFIER=$(./yq '.device_identifier' $CONFIG_FILE)
API_KEY=$(./yq '.api_key' $CONFIG_FILE)


if [ "$DEVICE_IDENTIFIER" = "\"\"" ]; then
    echo "DEVICE_IDENTIFIER was not set, generating from CPU Serial..."
    DEVICE_IDENTIFIER=$(awk '/Serial/ {print $3}' /proc/cpuinfo)
fi

sudo apt u

#Reading Config
CONFIG_FILE="config.yaml"

sudo apt update
sudo apt install libzbar0

python3 -m venv .venv --system-site-packages
source .venv/bin/activate

pip install -r requirements.txt

python3 setup.py $ROOM_NAME $DEVICE_IDENTIFIER $API_KEY

echo "Finished setting up student attendance tracker on this device!"