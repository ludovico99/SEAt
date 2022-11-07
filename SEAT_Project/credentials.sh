#!/bin/sh

echo \
"[default]
aws_access_key_id=ASIA2UH6LIUU4GHM44E2
aws_secret_access_key=KPVTi0VUrTMyKuj5iLZLWL7NeZ/ERBwWvY3HdeeD
aws_session_token=FwoGZXIvYXdzEC0aDAKa9J+OGouKcgCWTSLSAZ0Q0HloigT9FaGL7oClRy3Xwdhb9sZ5P8MzT6n99lGo2pQUX4/1oHSH3tm0kmaQaoVl5cr+g0zLRsoIGcfSzMDUm00T2fcExEbjpwKYLyVreE9XjNM8pVZ/Uk3HYkcrAnMBrPbjn5Vuy+u0MxAMEbsiptVN0wVyNvHiEaTbXGH5Z1aqShjPZgRqMMXq/ofcmZ18qaC0z2iYwdyd5FkVlOEw3VOfKEkyJUK6aQDZuPBadZTsIYCDXrLifRDdW8ArWoOhsdDHwc7zEt4XEP762yXYxCjMu56bBjItStWxe0T33iWxE+uIkq9zDlz6154tK0H2pLy7NcQpIsyWbxqdN3EyERxJ8+UG" > $HOME/.aws/credentials 

cp $HOME/.aws/credentials ./accountingService/credentials
cp $HOME/.aws/credentials ./quoteService/credentials
cp $HOME/.aws/credentials ./reservationService/credentials
cp $HOME/.aws/credentials ./reviewService/credentials
cp $HOME/.aws/credentials ./serviceRegistry/credentials