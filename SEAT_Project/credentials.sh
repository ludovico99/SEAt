#!/bin/sh

echo \
"[default]
aws_access_key_id=ASIA2UH6LIUUXLE3MYGN
aws_secret_access_key=8n/CusyYaZcXCAbm6NXr4mAOUDwap81u0r6a0+DX
aws_session_token=FwoGZXIvYXdzEHcaDMn+k7JYRX/D1Bmc4CLSAf4G/yQtcqr8waL70ZXKZgpDXtr4OUg9kJg7Alr+dIbwW/QJmRJtRetgKjlCtk41FwDvHTbqhXvaxyudLriliwMztrt8d65gHFMJ7gvbexl/2gfzCOxsu0OJpquiK/ILt7F0eTGUjJ5AiRLToKxxFE/KJxXsNwMBXfIz4nleiTFSEVqtR8la9tAKOD310O8RTj/HGL8apxtm7ZSX9nAkTgpdT5ooExcgNERPI0e3xDXEEN7V2agC8Kh+f+PIHM8T/PxqFzzZ/QQNwU8ILOSVCIhNdiiX1K6bBjItvrPvGsBIMLWqPBYK+UEHC4qPeubkvouaQ4ohvTOneqNvZexqnUkAPrYrDt1I" > $HOME/.aws/credentials 

cp $HOME/.aws/credentials ./accountingService/credentials
cp $HOME/.aws/credentials ./quoteService/credentials
cp $HOME/.aws/credentials ./reservationService/credentials
cp $HOME/.aws/credentials ./reviewService/credentials
cp $HOME/.aws/credentials ./serviceRegistry/credentials
cp $HOME/.aws/credentials ./paymentService/credentials