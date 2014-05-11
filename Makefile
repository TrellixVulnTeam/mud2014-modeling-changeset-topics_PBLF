all:
	nosetests

init:
	virtualenv --python=python2 env
	. env/bin/activate && pip install -r requirements.txt

requirements:
	pip install -r requirements.txt
