.PHONY: tests # `make tests` doesn't run because of the tests directory
PROGRAM=falc
COMMAND_TO_TRIGGER=fw
LOCAL_PIP_PATH=$(shell python3 -m site --user-site)

init: init_script init_tests

init_script:
	@echo INSTALLING SCRIPT REQUIREMENTS
	pip3 install -r requirements.txt --user

init_tests:
	@echo INSTALLING UNIT TEST REQUIREMENTS
	pip3 install -r test-requirements.txt --user

run:
	sudo PYTHONPATH=$(LOCAL_PIP_PATH) python3 -m $(PROGRAM).$(PROGRAM) $(COMMAND_TO_TRIGGER)

tests:
	PYTHONDONTWRITEBYTECODE=x pytest --cov=$(PROGRAM)

deb-eval-py3:
	./package-py3.sh deb
