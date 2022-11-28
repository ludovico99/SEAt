#!/bin/sh

# GROUP="docker"

# /bin/egrep  -i "^${GROUP}:" /etc/group
# if [ $? -eq 0 ]; then
#    echo "Group $GROUP exists in /etc/group"
# else 
#    echo "Group $GROUP does not exists in /etc/group"
#    sudo groupadd docker
# fi

# sudo usermod -aG docker $USER

cp -r /home/ubuntu/.aws/ /root/

sudo chmod +x /usr/local/bin/docker-compose

cd "/home/ubuntu/SEAT_Project/"

export SCALE_FACTOR=3
echo "SCALE_FACTOR=$SCALE_FACTOR" > config/.env

docker-compose --env-file=./config/.env up --scale payment=$SCALE_FACTOR --build
