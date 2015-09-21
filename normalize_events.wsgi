#!/usr/bin/python

app_name = "normalize_events"

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,'/var/www/' + app_name + '/')

import os
import site
# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('~/var/www/' + app_name + '/venv/local/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/var/www/' + app_name)
sys.path.append('/var/www/' + app_name + '/' + app_name)

# Activate your virtual env
activate_env=os.path.expanduser('/var/www/' + app_name + '/venv/bin/activate_this.py')
execfile(activate_env, dict(__file__=activate_env))

from normalize_events import app as application
application.secret_key = 'Add your secret key'
