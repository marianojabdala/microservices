#!/bin/bash

set -ex

export HOME="/root"
export APP_HOME="/usr/local"

cd $HOME

# Install pyenv
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> $HOME/.bash_profile
echo 'eval "$(pyenv init -)"' >> $HOME/.bash_profile
echo 'eval "$(pyenv virtualenv-init -)"' >> $HOME/.bash_profile

source $HOME/.bash_profile

#Install python 3.6.0
pyenv install 3.6.0

git clone https://github.com/marianojabdala/microservices.git $APP_HOME/app

cd $APP_HOME/app/users

#Creates a new virtual env
pyenv virtualenv python-virtual

#Activate new python environment
pyenv activate python-virtual

#upgrade pip
pip install pip --upgrade

#Install the requirements
pip install -r requirements.txt

make run
