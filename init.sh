#!/bin/sh

virtualenv --python=python venv
source venv/bin/activate

pip install -r requirements.txt

deactivate