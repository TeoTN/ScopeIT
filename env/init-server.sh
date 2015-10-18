#!/bin/bash
SHELLRC='/home/vagrant/.bashrc'
if ! grep -q 'PATH' "$SHELLRC"; then
	echo 'export PATH=$PATH:/usr/pgsql-9.4/bin/' >> $SHELLRC
	echo "alias scopeit='cd /home/vagrant/ScopeIT/src/; source ../env/scopeit/bin/activate; python manage.py runserver 0.0.0.0:1111'" >> $SHELLRC
fi
source $SHELLRC

PUPPET="/opt/puppetlabs/bin/puppet"
PUPPET_MODULES=("puppetlabs-postgresql" "stankevich-python")

for MODULE in ${PUPPET_MODULES[*]}
do
	eval $PUPPET module install $MODULE --modulepath /home/vagrant/ScopeIT/env/modules/
done
eval $PUPPET apply --modulepath=/home/vagrant/ScopeIT/env/modules /home/vagrant/ScopeIT/env/manifests/default.pp

#Temporary workaround: flush all from firewall
sudo iptables -F
