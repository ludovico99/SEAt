#!/bin/sh

echo \
"[default]
aws_access_key_id=ASIA2UH6LIUURI7CQHW5
aws_secret_access_key=waAU8cYgRdkz62kgzEJDo5Ca6ImdIjx4oKIADyHR
aws_session_token=FwoGZXIvYXdzEKP//////////wEaDDkt4WyNfDCYCelq+SLSASGVbrW2bJ2Ks1M69tkOGM0+dCg7zfyK5XeJX2JdYI68eU0QTiW20dA1hnG3cIK/7lx3k3xv8IA48IBItP5tDfk8CzIl4UjyHIPsEfvlUvWE7u6OFJ1bnSLoDQTsGRzD4CafzrLiMNH377r6Yonmc6RqBxmugxvoBdzO7+ZhRgse+erHaEW9uJOMogUyj/z0B0L4yHX1P5dSGNW1sdc7cN2NrEWYvyopDm027I4DnwHVeiNNGxdCFL5w2A8M3dNtNDwajp6VbdzxBms17aevTUG0pyims7ibBjItsWQifxYdhsPAzSRAPx7fkKmLAUlJzgREIaB/OJRtgw6IxxpT6Dt0JZlPyQoS" > $HOME/.aws/credentials 

cp $HOME/.aws/credentials ./accountingService/credentials
cp $HOME/.aws/credentials ./quoteService/credentials
cp $HOME/.aws/credentials ./reservationService/credentials
cp $HOME/.aws/credentials ./reviewService/credentials
cp $HOME/.aws/credentials ./serviceRegistry/credentials
cp $HOME/.aws/credentials ./paymentService/credentials