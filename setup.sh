# Ensure that pip being installed
python3.8 -m pip install --user --upgrade pip

# Install virtualenv
python3.8 -m pip install --user virtualenv

# Set up virtualenv
python3.8 -m venv venv

venv/bin/pip install -r requirements.txt