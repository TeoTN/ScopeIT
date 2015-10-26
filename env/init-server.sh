#!/bin/bash
SHELLRC='/home/vagrant/.bashrc'
ENV='/home/vagrant/ScopeIT/env/'

if ! grep -q 'PATH' "$SHELLRC"; then
	echo 'export PATH=$PATH:/usr/pgsql-9.4/bin/' >> $SHELLRC
	echo "alias scopeit='cd /home/vagrant/ScopeIT/src/; python manage.py runserver 0.0.0.0:1111'" >> $SHELLRC
	echo "alias python='/usr/bin/python3.4'" >> $SHELLRC
fi
source $SHELLRC

PUPPET="/opt/puppetlabs/bin/puppet"

while read MODULE; 
do
	eval $PUPPET module install $MODULE --modulepath /home/vagrant/ScopeIT/env/modules/
done < ${ENV}Modulesfile
eval $PUPPET apply --modulepath=/home/vagrant/ScopeIT/env/modules /home/vagrant/ScopeIT/env/manifests/default.pp

#Temporary workaround: flush all from firewall
sudo iptables -F
