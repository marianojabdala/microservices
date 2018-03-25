#!/usr/bin/env bash
set -ef
#Installl required packages  for pyenv to work properly.

sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev

sudo iptables -t nat -A PREROUTING -p tcp --sport 80 -j --dport localhost:8000

#Install pyenv
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> $HOME/.bash_profile
echo 'eval "$(pyenv init -)"' >> $HOME/.bash_profile
echo 'eval "$(pyenv virtualenv-init -)"' >> $HOME/.bash_profile

source $HOME/.bash_profile

#Install python 3.6.0
pyenv install 3.6.0

#Creates a new virtual env and activate it
pyenv virtualenv python3 && pyenv activate python3

#Install the requirements
pip install -r users/requirements.txt
