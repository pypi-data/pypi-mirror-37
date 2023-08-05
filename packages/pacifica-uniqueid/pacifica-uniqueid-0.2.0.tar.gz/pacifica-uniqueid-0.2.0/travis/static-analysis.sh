#!/bin/bash
pylint --rcfile=pylintrc UniqueIDServer.py DatabaseCreate.py uniqueid setup.py
radon cc *.py uniqueid
