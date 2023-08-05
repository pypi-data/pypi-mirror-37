%(name)s
========

  %(description)s


Usage
-----

  # Build the virtualenv and install required modules,
  # including this one in editable mode
  # Python 3
  0/make_venv3.sh
  # Python 2
  0/make_venv2.sh

  . venv/bin/activate

  # Build the module
  0/build.sh

  # Register the built module with PyPI
  0/register.sh

  # Upload a new build to PyPI
  0/upload.sh

  # Delete all built files
  0/clean.sh


Development
-----------

Run `0/make_venv3.sh` or `0/make_venv2.sh` first 

  . venv/bin/activate
  # This IPython config will set autoreload
  ipython --config=0/ipython_config.py

