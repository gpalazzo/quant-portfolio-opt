# base
sudo passwd ubuntu #asks for a new password to execute su commands

# technologies already installed by default: git, vim

# update
sudo apt update

# base
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt update

# install python
sudo apt-get install python3.7

# miniconda for virtual env
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh && rm -rf ./Miniconda3-latest-Linux-x86_64.sh
echo 'export PATH="/home/ubuntu/miniconda3/bin:$PATH"' >> ~/.bashrc

# postgres database
sudo apt install postgresql postgresql-contrib

# docker
sudo apt install apt-transport-https ca-certificates curl software-properties-common #install pre-requisites
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - #GPG key
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt update #update the installed packages
apt-cache policy docker-ce
sudo apt install docker-ce #docker installation
sudo systemctl status docker #verify if docker is active
sudo usermod -aG docker ${USER} #add current logged user to docker group to avoid using sudo everytime
su - ${USER}
id -nG #verify the user was added

# docker-compose v1.29.2
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# htop
sudo snap install htop
