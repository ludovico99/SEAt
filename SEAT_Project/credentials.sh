#!/bin/sh

echo \
"[default]
aws_access_key_id=ASIAZSPXN3SFTYKD5QL2
aws_secret_access_key=m7A9yw2sbnJLN87gQcj2qK+io1kbiwtnhKLDDypl
aws_session_token=FwoGZXIvYXdzEOT//////////wEaDI+mLW6Q027Y7pqrkCLXAVh20LrSwcv+4mx9cmeoWWHoUeysOCcUsEWWtUSDMLeENiCjayZc8ME23yapXIkIpJRnxbxNB/ed8KQY3RdGpZpdumXjrYdb2zb0KGFpNGFbzYgotoKPUOzre/P2iKwlGMtA/e7YFo9Ol2jkefSsuJ4VKYVFlMP3ukkCGVoSrDdGe9Iz49sVrAqtqoKeGXxYKh9rIpzVNDMXjvf0rNRqifR1ybxHBNmWygkdLgnLfPXFQyAb5IIFZng0GU1NGbspSr1ghjOZ2mQSGulW8CobAVfw3tO60Oc5KIu8jpsGMi1vaT7PlS6Xu/IB3XYQQpSOQNmFNcoBVcTnzpIpvwT9NpUQ5TE/W/SQTNxgoxM=" > $HOME/.aws/credentials 

cp $HOME/.aws/credentials ./accountingService/credentials
cp $HOME/.aws/credentials ./quoteService/credentials
cp $HOME/.aws/credentials ./reservationService/credentials
cp $HOME/.aws/credentials ./reviewService/credentials