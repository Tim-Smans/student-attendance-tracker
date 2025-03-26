sudo apt update
sudo apt install libzbar0

python3 -m venv .venv --system-site-packages
source .venv/bin/activate

pip install -r requirements.txt

echo "Finished setting up student attendance tracker on this device!"