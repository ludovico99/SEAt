#!/bin/sh
cd /home/ubuntu/SEAT_Project/
sudo docker-compose up --scale payment=2 --build
