#!/bin/bash

NAME="raqmn"                               # Name of the application
DJANGODIR=/home/ubuntu/raqmn         # Django project directory
BINDFILE=0.0.0.0:8000 # we will communicte using this binding
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=raqmn.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=raqmn.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source ../../../btp_venv/bin/activate # Virtual Directory path
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
# RUNDIR=$(dirname $SOCKFILE)
# test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../../../btp_venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --bind=$BINDFILE \
  --log-level=debug \
  --log-file=-
  --reload
  