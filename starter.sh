#!/bin/bash
export DJANGO_SECRET_KEY='@4Kk+;uel3)]JD&PKE2k(qSx/s(60H-c/A3[y@N1-l!2B8$P^}'

PROJECT_DIR=/home/vagrant/ScopeIT/
cd $PROJECT_DIR
source env/scopeit/bin/activate
pip install -r requirements.txt
cd src/
python manage.py runserver 0.0.0.0:1111 --settings=config.settings.dev_settings
