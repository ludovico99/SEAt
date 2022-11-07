cd terraform
terraform init
terraform apply -auto-approve 
TABLE=$(terraform output tables)
echo $TABLE
QUEUE=$(terraform output queue)
IPADRR_str=$(terraform output instance_public_ip)
IPADRR=$( echo $IPADRR_str | awk '{print substr($0, 2, length($0) - 2)}' ) 


cd ../

echo "[web]
$IPADRR ansible_user='ubuntu' ansible_ssh_private_key_file='/home/ludovico99/Scrivania/me-key.pem'" > hosts.ini

# echo "[web]" > hosts.ini
# echo $IPADRR_str | awk '{print substr($0, 2, length($0) - 2)}' >> hosts.ini
# echo "ansible_user='ubuntu' ansible_ssh_private_key_file='/home/ludovico99/Scrivania/me-key.pem'" >> hosts.ini

# ansible-playbook -v -i hosts.ini deploy.yaml
