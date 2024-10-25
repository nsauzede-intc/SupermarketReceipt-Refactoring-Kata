#!/usr/bin/env bash

[ ! `which texttest` ] && . .ensure_venv
TEXTTEST_HOME=. texttest -con
#pytest
pytest --approvaltests-use-reporter='PythonNative'
