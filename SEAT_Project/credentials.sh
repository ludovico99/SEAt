#!/bin/sh

echo \
"[default]
aws_access_key_id=ASIA2UH6LIUUQI7Y7ENK
aws_secret_access_key=eHIIv8PlFD9aZfAD3e9kbdkhDTvad39Os/I8+xyB
aws_session_token=FwoGZXIvYXdzEF8aDEH6Smj+2S194EZo3iLSAUDFKB9l3hZ+LpsD1AX1GicveCBQWQDX+itooVs1MBWqQB6QLj+x+DTQ+6YDDGhn5+6im0r+NloSU/Qo8sAWnhCJ9kgc77NaFDPzGYapSrdbt0cTP0ZQy4bfR835lbyjopk4HA4EQjbzDnDGaPQsl7qbQZsrz98YVhGAFJggJTYphzXhENiGkyBXkKXpdGxc8NNYz90jmLfnVM7C0n+Q6f+AmO1nNV3rV3JN2ahU/HZuohTyErFoLo4QuqFhj4dMRr4jzedDRL1ramb7hcz/MeXz7iiBrambBjIt262DAO35BOpCB27Zg7Zr8Oz4nMA/5I+3NVV2TpJtLCgJAqwT7YtzfR/t2N+m" > $HOME/.aws/credentials 

cp $HOME/.aws/credentials ./accountingService/credentials
cp $HOME/.aws/credentials ./quoteService/credentials
cp $HOME/.aws/credentials ./reservationService/credentials
cp $HOME/.aws/credentials ./reviewService/credentials
cp $HOME/.aws/credentials ./serviceRegistry/credentials
cp $HOME/.aws/credentials ./paymentService/credentials