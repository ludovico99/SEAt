#!/bin/sh

SSH="/home/ludovico99/Scrivania/me-key.pem"
PROJ_DIR="/home/ludovico99/Scrivania/SEAt/SEAT_Project"
IPADDR=$( cat $PROJ_DIR/hosts.ini | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" )

sudo scp -v -i $SSH -r $PROJ_DIR ubuntu@$IPADDR:/home/ubuntu
sudo ansible-playbook -v -i hosts.ini deploy.yaml