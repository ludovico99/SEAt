#!/bin/sh

echo \
"[default]
aws_access_key_id=ASIAZSPXN3SFVPXAVZNX
aws_secret_access_key=UHMdbe96kChUG5Np+2K6Ii6ITLjwex0iPyXOAq+/
aws_session_token=FwoGZXIvYXdzEIf//////////wEaDFXzO5kj/Yk1oq/SgSLXAQKkBT6ujJ4I/1zr5rM1G72A/mvCyoXa5Cdcev89h/ITG0jIBjdP32DrdnEKVE6N4w/uABWnas3IeUgy7ySHwDRX0vMYhMRrxlB3uTgtrccZidJhakfnZ959ntKmpCztc9JQluKuWjzJyzrCAQ6VmaUcE0g0FlIwdz8V/TPIUJp3CLzfSfYw0fd7fuKi60Aae8FZbno+y3SZ0jYSrwQasOaWYUbCHON4f9lZkvPZk+pFqVKKWt/MAl6XFYUIRKFdIBlIWczReSJ1HK+En0LutcLZtMlfkUKyKInu+ZoGMi1aCnM/ilbo8iyD3qLNlY3L0UpCU/7ZnpSMgWGHbCaeiiZqsdgrT3D6SN4GbiI=" > $HOME/.aws/credentials 

cp $HOME/.aws/credentials ./accountingService/credentials
cp $HOME/.aws/credentials ./quoteService/credentials
cp $HOME/.aws/credentials ./reservationService/credentials
cp $HOME/.aws/credentials ./reviewService/credentials