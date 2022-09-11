#!/bin/bash

# Uvicorn thingies
python certificates_backend/deleter.py &
  
# Start the second process
#gunicorn certificates_backend.__main__:app --workers 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
uvicorn certificates_backend.__main__:app  --host 0.0.0.0 --port 8000 &
  
# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?