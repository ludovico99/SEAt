# ssh = '/home/ludovico99/Scrivania/me-key.pem'
SSH='/home/elisa/Scrivania/SEAt_keys.pem'
PROJ_DIR = "/home/elisa/Scrivania/SEAt/SEAT_Project"

cd terraform
terraform init
terraform plan -var-file="terraform.tfvars"
terraform apply -auto-approve 
TABLE=$(terraform output tables)
QUEUE=$(terraform output queue)
IPADRR_str=$(terraform output instance_public_ip)
IPADRR=$( echo $IPADRR_str | awk '{print substr($0, 2, length($0) - 2)}' ) 


cd ../

echo "[web]
$IPADRR ansible_user='ubuntu' ansible_ssh_private_key_file=$SSH" > hosts.ini

chmod 400 $SSH
#sudo scp -i '/home/elisa/Scrivania/SEAt_keys.pem' -r "/home/elisa/Scrivania/SEAt/SEAT_Project" ubuntu@52.91.50.151:/home/ubuntu

#sudo scp -i $SSH -r $PROJ_DIR ubuntu@$IPADRR:/home/ubuntu
#sudo ansible-playbook -v -i hosts.ini deploy.yaml
