#!/bin/sh

echo \
"[default]
aws_access_key_id=ASIAZSPXN3SF2ZXJMLPK
aws_secret_access_key=Hm8oEnvj+izpc8V+i5L4xNe6IMvYz2nPVmpKs1jL
aws_session_token=FwoGZXIvYXdzEBMaDEbrvLonpKJCHqegGyLXAYxWUW+rL448ikdyCihs1xZZCEf/Ltw02l1HiezoNsPd0wMHwp3ICQMe1k8fxjhA5Crr89hetV+FFBWdEuVq/QvQwuFuIKMdCg/2RdBCU0burejwg9k/Z7GSk1j6W5tHZLqFu1aDgqaPazKho7eiLTSCg6ByKLM6f9bKk4+ThmiJyOHiGpIb8lQ/uGDXTyXfigfodvoCc6kvrx1FwCjBvlL+0yBr2WsjNdEd7iCyklnf9HvLXeFJWM2XUj6SO0ksiYuRgIxaw3oCR8X9x5JvsSldLbI2wayXKIjhmJsGMi0PeIqeO4w1/QxDuOcsbNzvojM+/yCgO+WX7k5e1S/mhNDBTX2HexDuu1gy5Rg=" > $HOME/.aws/credentials 

cp $HOME/.aws/credentials ./accountingService/credentials
cp $HOME/.aws/credentials ./quoteService/credentials
cp $HOME/.aws/credentials ./reservationService/credentials
cp $HOME/.aws/credentials ./reviewService/credentials