sudo apt-get install git librados-dev mongodb npm nodejs nodejs-legacy supervisor mercurial curl python-dev python-pip build-essential
sudo npm install -g bower react-tools
curl https://install.meteor.com/ | sh
sudo service mongodb start

# GO Setup
# Go to https://golang.org/doc/install?download=go1.5.1.linux-amd64.tar.gz
# Download go tar
wget https://storage.googleapis.com/golang/go1.4.2.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.4.2.linux-amd64.tar.gz
# edit .profile in your home directory
nano ~/.profile
# add the following line
export PATH=$PATH:/usr/local/go/bin

mkdir raqmn
cd raqmn
mkdir go
cd go

# add the following line to ~/.profile
export GOPATH=$HOME/raqmn/go
export PATH=$PATH:$GOPATH/bin

# Installing Quasar (now BtrDb)
go get github.com/SoftwareDefinedBuildings/btrdb/server
cd ~/raqmn/go/src/github.com/SoftwareDefinedBuildings/
rm -rf quasar
mv btrdb quasar
cd quasar
git checkout 0358bb4
go get ./... && go install ./qserver
# Edit qserver.conf
# replace filepath by /home/ubuntu/raqmn/data/quasar_data/quasar/
cd ~/raqmn
mkdir data
cd data
mkdir quasar_data
cd
cd raqmn/go/src/github.com/SoftwareDefinedBuildings/quasar
sudo mkdir /etc/quasar
sudo cp quasar.conf /etc/quasar/quasar.conf
qserver -makedb

# Installing Giles
go get -u -a github.com/gtfierro/giles
cd raqmn/go/src/github.com/gtfierro/giles
go get ./... && go install -a github.com/gtfierro/giles
curl -O https://raw.githubusercontent.com/gtfierro/giles/master/giles.cfg
cp giles.cfg raqmn/go/bin/ 

mkdir raqmn/log
# Add quasar.conf and giles.conf to /etc/supervisor/conf.d/

# Setting up plotter
mkdir raqmn/utils
cd raqmn/utils
git clone https://github.com/SoftwareDefinedBuildings/upmu-plotter.git
# Do changes in files
# Setup plotter.conf in supervisord

#Setting up deckard
cd 
cd raqmn/utils
git clone https://github.com/gtfierro/deckard.git
sudo npm install
bower install
jsx -w react_src/ public/build/
# Setup deckard.conf in supervisord

pip install django
pip install djangorestframework
pip install markdown       # Markdown support for the browsable API.
pip install django-filter  # Filtering support
sudo apt-get install libcurl4-openssl-dev
pip install pycurl
pip install requests
