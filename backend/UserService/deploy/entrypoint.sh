#!/bin/sh
cd $WORK_DIR
# Check if the first argument is empty
if [ -z "$1" ]; then
  echo "No argument provided, running default entrypoint"
  chmod a+x "deploy/entrypoints/docker-entrypoint.sh"
  exec deploy/entrypoints/docker-entrypoint.sh
else
  script="deploy/entrypoints/docker-entrypoint-$1.sh"
  if [ -f "$script" ]; then
    chmod a+x $script
    echo "Running $script"
    exec "$script"
  else
    echo "Script $script not found!"
    exit 1
  fi
fi
