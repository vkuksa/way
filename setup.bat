rem Ensure that pip being installed
py -m pip --version

rem Install virtualenv
py -m pip install --user virtualenv

rem Set up virtualenv
py -m venv venv
.\venv\Scripts\activate

pip install -r requirements.txt
