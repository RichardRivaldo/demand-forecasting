#!/bin/bash
pip install -r requirements.txt --no-cache-dir
uvicorn main:app --host 127.0.0.1 --port 8000
