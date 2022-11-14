#!/bin/sh
cd /home/ubuntu/SEAT_Project/

export SCALE_FACTOR=3
echo "SCALE_FACTOR=$SCALE_FACTOR" > config/.env
sudo docker-compose --env-file=./config/.env up --scale payment=$SCALE_FACTOR --build
