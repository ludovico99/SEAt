#!/bin/sh

echo \
"[default]
aws_access_key_id=ASIAZSPXN3SFUHVMFJM5
aws_secret_access_key=zxDEAQdFaXJ1bkUPRAthmLcm+Vmf9jNu3um1QLZN
aws_session_token=FwoGZXIvYXdzEEwaDC1ZpJrmXFbWqmi/PiLXAT1D/Y0fwXTJ+cW9FHQJN+1tfQ3QohmAlkXzgfUP+1s3leo/Q+SeR/ZvraUJT2HGkgpdS3e4Z2k6C0HRrA69gcee2pk5HwS3evBRFsOKPx0gdpLvCejPVUJEJaEB27XcFh3glUExRVS02JIBwuGpNPiiIZmf6DBqKgrN1SR6ZxO4jJsZkmw5ERshXTGCWJx11W3Vj8ymfBM3KwTDHtIldhwNrJLf1j2cIOrpeCqIa3ip77jdw+LCP+ihNtGAFTc1UsqvUEQ2morANynlj6rS+OAdSiwmrfMeKP6SpZsGMi2QzOOEJieUSJoDEXcwhpMSxYUhB8FEGwMjHdZDarGRVZ4o3RgXSPuIq2+0vS8=" > $HOME/.aws/credentials 

cp $HOME/.aws/credentials ./accountingService/credentials
cp $HOME/.aws/credentials ./quoteService/credentials
cp $HOME/.aws/credentials ./reservationService/credentials
cp $HOME/.aws/credentials ./reviewService/credentials
cp $HOME/.aws/credentials ./serviceRegistry/credentials
cp $HOME/.aws/credentials ./payment/credentials