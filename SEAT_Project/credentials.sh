#!/bin/sh

PROJ_DIR="/home/ludovico99/Scrivania/SEAt/SEAT_Project/"

echo \
"[default]
aws_access_key_id=ASIAZSPXN3SFR3TL3E77
aws_secret_access_key=DJnIGSxccGPLiZJ2EHr+5KmqE/Hh6wjIaMNsODeK
aws_session_token=FwoGZXIvYXdzED4aDKxWL4GNMXtrQrBwxyLXAbfDnvmHau7glP4RLxq5ddOKQPorRr6qHMy1S7+prZuaq25phPL9QzaormIqbqIAGhlr0EVrJokS6V3yaioLHKAstg5MFDo/x8ROg6VnxExzQMCJ/AJrOtFUc6m+uhkCGebxofNchklFiqquyHC5Baf6uVp2Rk/7sgSvjsZcuIZUC70EJ9DfARSeLyon57t+98DF04bJK8ipyvl/Nc1Vl7OpGsjNsFMnGZfdJ/juk68sESc79KXYEu/93URQ8YFURmJ7T3yEixnFx7f8Z0SXhVxmPZOzj3RhKP6s2psGMi3WTZOMtkNcE1rHgOzn5JTe46U+5FG98IukRZ4iqhuJn2PkGgH/BUaBR2UvpGY=" > $HOME/.aws/credentials 

# cd $PROJ_DIR

# cp $HOME/.aws/credentials ./accountingService/credentials
# cp $HOME/.aws/credentials ./quoteService/credentials
# cp $HOME/.aws/credentials ./reservationService/credentials
# cp $HOME/.aws/credentials ./reviewService/credentials
# cp $HOME/.aws/credentials ./serviceRegistry/credentials
# cp $HOME/.aws/credentials ./paymentService/credentials