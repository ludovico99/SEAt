#!/bin/sh

echo \
"[default]
aws_access_key_id=ASIA2UH6LIUU74NTFWMK
aws_secret_access_key=U1rrSk1pNNLxnXgLBG5jMasogoMUbs35jDiP/jOR
aws_session_token=FwoGZXIvYXdzEND//////////wEaDKh8bNIls91RNZgTxCLSAT3pzVJMLJVQnmV8Xmgcw9gsEWOpsdzMAy7iUuLtR8EIVOY+d8iBIAHe7q6AiqVxqA61hBvugC+sGzg7eMHee+xjgxFQAyvHDI0RqA3Hcrzxd1I5++IMNMfw45f1IoU8rik6wCzurE97oL5BiktmSOR6+1LPRS7wLYuWhC27d/ZNXNzjTT3liuYl5+D/Qkws7kUpifzoDUm9gaBs1PsXexwsmBiSv3jyF8RESIdq8iKuNjMS5pxpE8tk8VR9l6D/O11XvFiidjQdQg02SA8DZOJpBiig+ombBjIt5jaQGhoNm0y9jVgYPW5F5mwWFIeEXxidU9M77nPiFzsWLsciPiXjP4HTHSZ4" > $HOME/.aws/credentials 

cp $HOME/.aws/credentials ./accountingService/credentials
cp $HOME/.aws/credentials ./quoteService/credentials
cp $HOME/.aws/credentials ./reservationService/credentials
cp $HOME/.aws/credentials ./reviewService/credentials