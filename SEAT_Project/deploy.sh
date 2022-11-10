SSH='/home/elisa/Scrivania/SEAt_keys.pem'
PROJ_DIR = "/home/elisa/Scrivania/SEAt/SEAT_Project"

sudo scp -i $SSH -r $PROJ_DIR ubuntu@$IPADRR:/home/ubuntu
sudo ansible-playbook -v -i hosts.ini deploy.yaml