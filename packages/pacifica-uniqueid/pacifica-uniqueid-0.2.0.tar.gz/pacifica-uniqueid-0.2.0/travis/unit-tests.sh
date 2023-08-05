#!/bin/bash -xe
export MYSQL_ENV_MYSQL_USER=root
export MYSQL_ENV_MYSQL_PASSWORD=
coverage erase
rm -vf .coverage.*
export MYSQL_ENV_MYSQL_DATABASE=pacifica_uniqueid2
coverage run -p DatabaseCreate.py
export MYSQL_ENV_MYSQL_DATABASE=pacifica_uniqueid
sudo service mysql stop
# fail to connect
coverage run -p UniqueIDServer.py || true
sudo service mysql start
sleep 5
coverage run -p -m uniqueid --stop-after-a-moment &
SERVER_PID=$!
while ! curl -s -o /dev/null localhost:8051
do
  sleep 1
done
coverage run -p -m pytest -v
wait

# break mysql after successfully starting
coverage run -p UniqueIDServer.py --stop-after-a-moment &
SERVER_PID=$!
sleep 2
curl 'localhost:8051/getid?range=10&mode=file' || true
sudo service mysql stop
sleep 1
curl 'localhost:8051/getid?range=10&mode=file' || true
wait

coverage combine -a .coverage.*
coverage report --show-missing --fail-under=100
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
