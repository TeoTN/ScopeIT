# -*- mode: ruby -*-
# vi: set ft=ruby :

$psql_user = 'root'
$psql_passwd = 'existenceprecedeessence'
$psql_db = 'scopeit'
$venv_path = '/home/vagrant/ScopeIT/env/scopeit/'
$req_path = '/home/vagrant/ScopeIT/requirements.txt'

include git

git::config { 'user.name' :
    value => 'Piotr Staniów',
}

git::config { 'user.email' :
	value => 'staniowp@gmail.com',
}

package { 'postgresql-server-dev-9.4':
	ensure 	=> installed,
} ->
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

package { 'python3.4-venv':
	ensure 		=> installed
} ->
class { 'python' :
	version 	=> '3.4',
	pip			=> 'present',
	dev 		=> 'present',
} ->
python::pyvenv { 'scopeit':
	ensure 		=> 'present',
	version 	=> '3.4',
	venv_dir 	=> $venv_path,
}

