#!/bin/sh

PROJ_DIR="/home/ludovico99/Scrivania/SEAt/SEAT_Project/"

echo \
"[default]
aws_access_key_id=ASIAZSPXN3SF3LASNDQ6
aws_secret_access_key=ql12gmabIhtUrooSea2vcXfWlgrqbdjSzDqwXuwO
aws_session_token=FwoGZXIvYXdzEO///////////wEaDMq0NP+gU9sEauNPBiLXAXBM0CWUhgUHgUxBHB6S3NzJvufrIyLzfMQtfEQaLdx3Zjw16beUGoCwqhrehB3Rj5i+M9i4q0RiZ6MtH8bS1H3wlrkm8Lg8eewKwY9a+BQX0v7yLPky39QYwJG3En1BE2kMyryu9f9TYJKWgs0zxj1H4hg/xtRE870fM+rUnY0b5CCaw2DNWPIp0kjHA/qaPuglq2s/mW6y5lHkfA5Tli/qdSkqNBJFHOxuJu3+U8tKHX//70WxTkLp5DRufJBWg0z0m4fjzEUZdeq2oYeiD+rjwfXu6fFLKIuIyZsGMi3bOCxFlNNz01zW20ypbZ8p0i7CEX5zuKCxk7ZwnkOeWHN7X2IKG1aX762HVBA=" > $HOME/.aws/credentials 

cd $PROJ_DIR

cp $HOME/.aws/credentials ./accountingService/credentials
cp $HOME/.aws/credentials ./quoteService/credentials
cp $HOME/.aws/credentials ./reservationService/credentials
cp $HOME/.aws/credentials ./reviewService/credentials
cp $HOME/.aws/credentials ./serviceRegistry/credentials
cp $HOME/.aws/credentials ./paymentService/credentials