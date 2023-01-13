PROGRAM=fall
LOCAL_PIP_PATH=$(shell python3 -m site --user-site)

init: init_script init_tests

init_script:
	@echo INSTALLING SCRIPT REQUIREMENTS
	pip3 install -r requirements.txt --user

init_tests:
	@echo INSTALLING UNIT TEST REQUIREMENTS
	pip3 install -r test-requirements.txt --user

tests:
	PYTHONDONTWRITEBYTECODE=x pytest --cov=$(PROGRAM)
