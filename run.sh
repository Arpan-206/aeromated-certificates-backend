#!/bin/bash

# Uvicorn thingies
# python certificates_backend/deleter.py &
  
gunicorn certificates_backend.__main__:app --workers 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:80 &# Start the second process

  
# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?