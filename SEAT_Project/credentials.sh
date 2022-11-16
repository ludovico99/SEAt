#!/bin/sh

PROJ_DIR="/home/ludovico99/Scrivania/SEAt/SEAT_Project/"

echo \
"[default]
aws_access_key_id=ASIAZSPXN3SF3UJXYEAN
aws_secret_access_key=DTl+WybjBw5VCO8JK8jdseEfRv+Z5WukFUAU0NOK
aws_session_token=FwoGZXIvYXdzEB8aDL+ZxoresV4yCXmYgyLXAcnepgvAG9chovoX0i4mtiluUmSoyfdbOLJjf8BaCCQUtMxJg/Psf7hiBtRlTMXv1sgJ3K7q44a2cUf+fouKOlWWDSbsg4kIFpB/BLpJ5byTa3ASxdk0Xvdb8iktciZe+uJ2HVyipAcrGLCQDW4fWVMnBtvDYupDxAYS7LOmIgxI77Sgkknh7tXt/q3x8A3s/No5u4tQ5dsekWM8RR9hG3jrWODlucOYFd6E7kzWLZ7OFga9DX9TjsZ9Fk81z3GNizARtT8UQoGRcaZPrS8+/P7IrBl/5UjMKJfK05sGMi3zT/aTSXCVVY6YAHIRkF2N+LEQ0TyrbZzhLxn/KXvWmRLx6idBT1JE/Fq5xxU=" > $HOME/.aws/credentials 

cd $PROJ_DIR

cp $HOME/.aws/credentials ./accountingService/credentials
cp $HOME/.aws/credentials ./quoteService/credentials
cp $HOME/.aws/credentials ./reservationService/credentials
cp $HOME/.aws/credentials ./reviewService/credentials
cp $HOME/.aws/credentials ./serviceRegistry/credentials
cp $HOME/.aws/credentials ./paymentService/credentials