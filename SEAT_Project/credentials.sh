#!/bin/sh

echo \
"[default]
aws_access_key_id=ASIA2UH6LIUUWBCFHNLH
aws_secret_access_key=OJuGRX/R5zaSI/doLctzHI64jcXLmM/vXqCWRHTU
aws_session_token=FwoGZXIvYXdzEOn//////////wEaDKyWt4ZKRMsn5gEv/yLSAZRq+JCJCk8ZLBYJYXE9H+9Pe+Uyv0GrqXk4airfnBdDmlMzADit0VYhg5KpNm+k170EqULnL4ygDtpvns1ZP/+K4UhhoIJXdMwTmXigoPG+FdrmuAPPWoiwc8FxMrUI4kgWtBDkuAW0sayriRlwkZDq0/f6w74kcpX6cUITGwjRNrr3A8c4CVthb8jSv9GtyRUJHLoIIPqxbVulzRUKblJ81iy8rKVMZe5VbbKNDf7Zf1NDH2i6gKJVXnEVKoFgViGcXjOmWoXmOwez1UWpaBkqISi8v4+bBjIt5FHCztirMtwTsYInWuErVpvzMfjZXBzHU1R3bXZ2tjWLCwF0GI3p1+rO1Mxc" > $HOME/.aws/credentials 

cp $HOME/.aws/credentials ./accountingService/credentials
cp $HOME/.aws/credentials ./quoteService/credentials
cp $HOME/.aws/credentials ./reservationService/credentials
cp $HOME/.aws/credentials ./reviewService/credentials