#!/bin/sh
pip install pytest flask --quiet
pytest test_app.py -v