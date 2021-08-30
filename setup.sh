#!/usr/bin/env bash
set -ef

#Installl required packages  for pyenv to work properly.
sudo apt-get update && sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev

#Install pyenv
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> $HOME/.bash_profile
echo 'eval "$(pyenv init -)"' >> $HOME/.bash_profile
echo 'eval "$(pyenv virtualenv-init -)"' >> $HOME/.bash_profile

source $HOME/.bash_profile

#Install python 3.9
pyenv install 3.9

#Creates a new virtual env
pyenv virtualenv python-virtual

#Activate new python environment
pyenv activate python-virtual

#upgrade pip
pip install pip --upgrade

#Install the requirements
pip install -r requirements.txt
