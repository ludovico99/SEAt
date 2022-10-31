#!/bin/sh

echo \
"[default]
aws_access_key_id=ASIA2UH6LIUUWYAWVP2C
aws_secret_access_key=uS9nYHy9pLc1YjAIHirmFvtU2mv1oVpI6unmoCwA
aws_session_token=FwoGZXIvYXdzEKP//////////wEaDIlco0qocq5rZgEx5CLSASgdofIf+zr5l25ab6NYZtfH8ln57b2BCU6NfRjEGWgOITvdn0MkafDagZYTe6QiHl5AODRR4xwVKIBCC+179Tvnr9Fnije+C8ZCsJ2+f9Wul+1yHIFyiHxwsii+dA13yU8aBppLc5LeFj0orUZFrJW2qw9p8+vOTDc9YAlV9WqLlnVHzYZ3APLUDijcRtRMfZjW8wmEz9kLYoftoGVj49x8BUZsDWin+Zu04dqqHrT8YRTvCNNwM68MSHnJ16bMy0DJeuWADK1nnonIR+orF0WQXyimk4CbBjIthKgyXX46RCHzgfmunoFeOwn9FieBzsz2pP2+5UVmfdHh+H8NlEJ/w6TQVZgC" > $HOME/.aws/credentials 

cp $HOME/.aws/credentials ./accountingService/credentials
cp $HOME/.aws/credentials ./quoteService/credentials
cp $HOME/.aws/credentials ./reservationService/credentials
cp $HOME/.aws/credentials ./reviewService/credentials