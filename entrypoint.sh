#!/bin/sh

mkdir -p /persist/cache

ln -s /persist/cache /cache
ln -s /persist/config.ini ./config.ini
ln -s /persist/database.db ./database.db

export PYTHONPATH=../

python main.py