# -*- mode: ruby -*-
# vi: set ft=ruby :

$psql_user = 'root'
$psql_passwd = 'existenceprecedeessence'
$psql_db = 'scopeit'
$venv_path = '/home/vagrant/ScopeIT/env/scopeit'

include git

git::config { 'user.name' :
    value => 'Piotr Staniów',
}

git::config { 'user.email' :
	value => 'staniowp@gmail.com',
}

package { 'postgresql-devel':
	ensure => installed
}

class { 'postgresql::globals':
	manage_package_repo => true,
	version             => '9.4',
} -> 
class { 'postgresql::server':
	listen_addresses  => '*',
	postgres_password => $psql_passwd,
}

postgresql::server::db { $psql_db:
	user     => $psql_user,
    password => postgresql_password($psql_user, $psql_passwd),
}

postgresql::server::pg_hba_rule { 'allow remote connections with password':
	type        => 'host',
    database    => 'all',
    user        => 'all',
    address     => 'all',
    auth_method => 'md5',
}

class { 'python' :
	version		=> 'system',
	pip			=> 'present',
    dev			=> 'present',
	virtualenv	=> 'present',
}

python::virtualenv { $venv_path :
	ensure			=> 'present',
	requirements	=> '/home/vagrant/ScopeIT/requirements.txt',
}

class { 'nodejs':
	nodejs_dev_package_ensure 	=> 'present',
	npm_package_ensure			=> 'present',
	repo_class					=> '::epel',
}

package { 'bower':
    ensure => 'present',
    provider => 'npm',
}

package { 'react':
    ensure => 'present',
    provider => 'npm',
    install_options => ['--save'],
    target          => '/home/vagrant/ScopeIT/src/static/js/build/',
}

package { 'react-dom':
    ensure => 'present',
    provider => 'npm',
    install_options => ['--save'],
    target          => '/home/vagrant/ScopeIT/src/static/js/build/',
}

package { 'babel':
    ensure => 'present',
    provider => 'npm',
    install_options => ['--save'],
    target          => '/home/vagrant/ScopeIT/src/static/js/build/',
}
