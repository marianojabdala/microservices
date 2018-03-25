#!/usr/bin/env bash
set -ef

#Installl required packages  for pyenv to work properly.
sudo apt-get update && sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev

#Enable route from 8000 to 80
sudo iptables -t nat -A PREROUTING -p tcp --sport 80 -j --dport REDIRECT 8000

#Install pyenv
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> $HOME/.bash_profile
echo 'eval "$(pyenv init -)"' >> $HOME/.bash_profile
echo 'eval "$(pyenv virtualenv-init -)"' >> $HOME/.bash_profile

source $HOME/.bash_profile

#Install python 3.6.0
pyenv install 3.6.0

#Creates a new virtual env
pyenv virtualenv python3

#Activate new python environment
pyenv activate python3

#Install the requirements
pip install -r users/requirements.txt
