#!/bin/sh

SSH='/home/elisa/Scrivania/SEAt_keys.pem'
PROJ_DIR="/home/elisa/Scrivania/SEAt/SEAT_Project"
IPADDR=$( cat $PROJ_DIR/hosts.ini | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" )

sudo scp -v -i $SSH -r $PROJ_DIR ubuntu@$IPADDR:/home/ubuntu

sudo scp -v -i $SSH -r $HOME/.aws/ ubuntu@$IPADDR:/home/ubuntu/.aws/

# sudo scp -v -i $SSH -r $PROJ_DIR/run.sh ubuntu@$IPADDR:/home/ubuntu/SEAT_Project/run.sh
cd $PROJ_DIR

ansible-playbook -v -i hosts.ini deploy.yaml
