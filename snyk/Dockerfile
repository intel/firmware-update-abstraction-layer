FROM snyk/snyk-cli:python-3.9
RUN python3 -m venv /venv3-snyk && . /venv3-snyk/bin/activate && python -m pip install -U pip
COPY scan-python.sh /scan-python.sh
RUN chmod +x /scan-python.sh

ENTRYPOINT []
