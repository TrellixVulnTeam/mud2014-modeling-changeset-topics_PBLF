all:
	nosetests

install: submodules

submodules:
	git submodule init
	git submodule update

update:
	git submodule foreach git pull origin master

init:
	virtualenv --python=python2 env
	. env/bin/activate && pip install numpy
	. env/bin/activate && pip install --editable lib/gittle
	. env/bin/activate && pip install --editable lib/whatthepatch
	. env/bin/activate && pip install --editable lib/gensim
	. env/bin/activate && pip install -r requirements.txt

requirements:
	pip install -r requirements.txt
