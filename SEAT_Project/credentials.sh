#!/bin/sh

PROJ_DIR="/home/ludovico99/Scrivania/SEAt/SEAT_Project/"

echo \
"[default]
aws_access_key_id=ASIA2UH6LIUU7WILNJMH
aws_secret_access_key=9QadS0fqDWaeSqhzTDfeU0x8mu/RtxZbnfsTUn4l
aws_session_token=FwoGZXIvYXdzEOD//////////wEaDLgm63m0DVBb7lCydSLSAQ/Y/Bzkb33GZkuaJwQR4jxAwvW5xpRHC7U5IyS1pzDchseY2ZeUpFoQ5202fX9dK3xc5ge51cXQhnoLGTFHgF14DEKIJqKpkzQe7nG05VHUV2tC5sTn7GFeBS2oRGOb+F2VUTO8QKJ15eJfZ2rKscc5IF0CEQd2kxBpgplhB4Apzn9JC9NE+9xQAIle6HgliC3TThb5dDFQwXMFzCpKc8N8if1j900mLcXUETxO6wQTrFBjZ+EG02woeU1Ovv6GlH+1q9GYHp6gmyWDrRlVwQtJEij9g/6bBjItTC1KcoJbvDSFtF8nJIROvpwAiWLlsUOqbd/EILWR5ANSdeZ2se/zwfxDQL2U" > $HOME/.aws/credentials 

# cd $PROJ_DIR

# cp $HOME/.aws/credentials ./accountingService/credentials
# cp $HOME/.aws/credentials ./quoteService/credentials
# cp $HOME/.aws/credentials ./reservationService/credentials
# cp $HOME/.aws/credentials ./reviewService/credentials
# cp $HOME/.aws/credentials ./serviceRegistry/credentials
# cp $HOME/.aws/credentials ./paymentService/credentials
