#bin/bash

AMI=ami-0149b2da6ceec4bb0
sg=sg-0e1f968a157148ba4

aws ec2 run-instances --image-id ${AMI} --count 1 \
--instance-type t2.micro \
--security-group-ids ${sg} \
--key-name me-key --associate-public-ip-address \
--tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=SEAt}]"



