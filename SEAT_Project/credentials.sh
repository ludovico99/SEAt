#!/bin/sh
PROJ_DIR="/home/ludovico99/Scrivania/SEAt/SEAT_Project/"

echo \
"[default]
aws_access_key_id=ASIAZSPXN3SF3W2KBGFD
aws_secret_access_key=vXPZ8RRbEJrcqieloarcAbr7fyE2FNUNKpPPXr+l
aws_session_token=FwoGZXIvYXdzEKf//////////wEaDK9GQG24J205RLq1zyLXASbi8DdqkQGcBNlJgm9/wi6FGTp/kVYJ9J5caX5gcIAbIAIkgngKWaqqoPUMJKjj8Y5p3c/H5vXo/TLAeRG0hWgP37FvGwffggw3U32JXn3k4/DpOYnwxgG9n6w+u4Z95nUTqm/5pxmpOT895LYwzgOD7TEMEZqwk7kUosy8UuUhugELUGe93sTHjrFp4ni5/VaCfuEp2NKRHoLJugt5dl5AnZ/dnBw99jrxOoxxvUFNOTBzCTWagIhIHsgMLrhK0+8AgSljNvPkAUY4UJUd2BrWH4oQ8z6aKOWTuZsGMi3YMZYcDW9L9HsRK5hpp4RGUiKS3V1a91W5gAgXn+X2VWfnKCpib59Z+ZR7BqQ=" > $HOME/.aws/credentials 

cd $PROJ_DIR

cp $HOME/.aws/credentials ./accountingService/credentials
cp $HOME/.aws/credentials ./quoteService/credentials
cp $HOME/.aws/credentials ./reservationService/credentials
cp $HOME/.aws/credentials ./reviewService/credentials
cp $HOME/.aws/credentials ./serviceRegistry/credentials
cp $HOME/.aws/credentials ./paymentService/credentials