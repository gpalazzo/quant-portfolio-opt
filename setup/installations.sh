#!/bin/bash

# base
sudo passwd ubuntu #asks for a new password to execute su commands

# technologies already installed by default: git and python

# update
sudo apt update

# miniconda for virtual env
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh && rm -rf ./Miniconda3-latest-Linux-x86_64.sh
export PATH="/home/ubuntu/miniconda3/bin:$PATH" >> ~/.bashrc

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

