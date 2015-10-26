# -*- mode: ruby -*-
# vi: set ft=ruby :

$psql_user = 'root'
$psql_passwd = 'existenceprecedeessence'
$psql_db = 'scopeit'
$venv_path = '/home/vagrant/ScopeIT/env/scopeit'
$req_path = '/home/vagrant/ScopeIT/requirements.txt'

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

package { 'python34' :
	ensure => 'installed'
}

package { 'python34-devel':
	ensure => 'installed'
}

exec { "install_pip":
	command		=> "wget https://bootstrap.pypa.io/get-pip.py; chmod +x ./get-pip.py; python3.4 get-pip.py",
	path 		=> ["/usr/local/bin/", "/bin/"]
}

exec { "install_requirements":
	command 	=> "pip install -r ${req_path}",
	path 		=> ["/usr/local/bin/", "/bin/"]
}

/*
class { 'nodejs':
	nodejs_dev_package_ensure 	=> 'present',
	npm_package_ensure			=> 'present',
	repo_class					=> '::epel',
}

package { 'bower':
    ensure => 'present',
    provider => 'npm',
}

nodejs::npm { 'react':
    ensure => 'present',
    install_options => ['--save'],
    target          => '/home/vagrant/ScopeIT/src/static/js/build/',
}

nodejs::npm { 'react-dom':
    ensure => 'present',
    install_options => ['--save'],
    target          => '/home/vagrant/ScopeIT/src/static/js/build/',
}

nodejs::npm { 'babel':
    ensure => 'present',
    install_options => ['--save'],
    target          => '/home/vagrant/ScopeIT/src/static/js/build/',
}
*/
