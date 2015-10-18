#!/bin/bash
cd /home/vagrant/ScopeIT/src/
source ../env/scopeit/bin/activate
./manage.py runserver 0.0.0.0:1111
