#!/bin/sh

echo \
"[default]
aws_access_key_id=ASIA2UH6LIUU3ZWIFA7G
aws_secret_access_key=lcb9gVvbH0pdnZlJiQciyqgvm74xHhzfPK3dchwG
aws_session_token=FwoGZXIvYXdzEPv//////////wEaDCTW3Oym3jNZWm+OnyLSAYEvRMviP/dhcDajpfpX+LvmV7vz/3jSELVEnYV+Ch3F9zvznX08vK3q67bOUWNlo2gzqgyVhfbW7Iq+5nqq4PrmuQ+iAhtMNR60/G/etczEsehm2PJ1X3OVtHEWM6xKDOa06r1A+fsvdlV8W2+rhZmEgH71lpFiIjVbgwTy5g0AHFjXQbRZjTM3KTlQ++oAxUGmqH+F0E97xS63TkCxPbySto50wWyx2aD+eFg2fKfWinB6VSh2Z+vWlvBxnaZTlX4TMtxo2N5dHZBRWTJSXStT+yiGu5ObBjIt/DqLTn/yrn39hp4dUTxqrorpU0tOqppN6iWtZs+2dJvHqa7TCBoj7Lk13Ahm" > $HOME/.aws/credentials 

cp $HOME/.aws/credentials ./accountingService/credentials
cp $HOME/.aws/credentials ./quoteService/credentials
cp $HOME/.aws/credentials ./reservationService/credentials
cp $HOME/.aws/credentials ./reviewService/credentials