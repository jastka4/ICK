all: setup

venv/bin/activate:
	if which virtualenv-2.7 >/dev/null; then virtualenv-2.7 venv; else virtualenv venv; fi

run: venv/bin/activate requirements.txt
	. venv/bin/activate; flask run --host 0.0.0.0

debug: venv/bin/activate requirements.txt
	. venv/bin/activate; flask run --host 0.0.0.0 --debugger --reload

setup: venv/bin/activate requirements.txt
	. venv/bin/activate; pip install -Ur requirements.txt

init: venv/bin/activate requirements.txt
	. venv/bin/activate; flask create
