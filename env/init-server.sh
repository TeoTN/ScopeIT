#!/bin/bash
SHELLRC='/home/vagrant/.bashrc'
if ! grep -q 'PATH' "$SHELLRC"; then
	echo 'export PATH=$PATH:/usr/pgsql-9.4/bin/' >> $SHELLRC
fi
source $SHELLRC

PUPPET="/opt/puppetlabs/bin/puppet"
PUPPET_MODULES=("puppetlabs-postgresql" "stankevich-python")

for MODULE in ${PUPPET_MODULES[*]}
do
	eval $PUPPET module install $MODULE --modulepath /home/vagrant/ScopeIT/env/modules/
done
eval $PUPPET apply --modulepath=/home/vagrant/ScopeIT/env/modules /home/vagrant/ScopeIT/env/manifests/default.pp

