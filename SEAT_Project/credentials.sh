#!/bin/sh

echo \
"[default]
aws_access_key_id=ASIAZSPXN3SF6PBRTWOY
aws_secret_access_key=WNlukdpR5rfHI8i8WjuANZISRS0jsOWzSsZ4nz5O
aws_session_token=FwoGZXIvYXdzEGAaDIE7E6dKE1DGjdK/tyLXAddZNauf+oDnqwmMllUWTix+lx8feoRjRWJge7InncEnyaUfJeZ2GXrtkkMtkGN8lK4YWsBo0ke0fQpWA0e0lkWoE4Q7tFFtKDDvsDAHrn+efy0f+P4GMn3FHAuhoLJ1XgtsvsgtAHj7BrgXMak/bh75t3XsGjKTXZzoVrDP749a/p74UMh9F+7mDt8ehEalzE2aY9kdz6+S7pSQq3cM3G/zzt+mbO4ByrbvbBcE8Hw9Oop/05OKTGD9+qsX7uyo5+o/Irj+h7wnDDIl0BfAb9i2qzWw8BegKJjcqZsGMi3xS1wlkriAocexWyjhqOykULWhqeJC1l2GTlcJ+41EzwCzNputqgs2X04TPHA=" > $HOME/.aws/credentials 

cp $HOME/.aws/credentials ./accountingService/credentials
cp $HOME/.aws/credentials ./quoteService/credentials
cp $HOME/.aws/credentials ./reservationService/credentials
cp $HOME/.aws/credentials ./reviewService/credentials
cp $HOME/.aws/credentials ./serviceRegistry/credentials
cp $HOME/.aws/credentials ./paymentService/credentials