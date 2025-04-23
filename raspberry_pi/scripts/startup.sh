#!/bin/bash

source .venv/bin/activate
python -m scripts.main

crontab -e

* * * * * /usr/bin/python3 -m scripts.ping_backend.py