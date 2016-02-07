# -*- mode: ruby -*-
# vi: set ft=ruby :

# Recommended pugins:
#   vagrant plugin install vagrant-cachier
# Caches package installation to a folder under ~/.vagrant.d
#
#   vagrant plugin install vagrant-faster
# Sets cpu/memory to a good value above default, speeds up VM.

$root = <<EOF
source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
sudo apt-get update -y
sudo apt-get install -y build-essential automake autopoint autoconf pkg-config cmake \
 ninja ccache git mercurial vim rar p7zip-full python-dev \
 ruby ruby-dev pandoc sphinx-common \
 silversearcher-ag rethinkdb npm tree \
 libyaml-dev libxml2-dev libxslt-dev zlib1g-dev \
 lubuntu-desktop

# Webpack expects node
sudo ln -s /usr/bin/nodejs /usr/bin/node

wget https://bootstrap.pypa.io/get-pip.py
sudo python ./get-pip.py
rm get-pip.py
sudo pip install -U Flask Flask-Cache PyYAML html5lib lxml nose python-dateutil requests rethinkdb termcolor
sudo pip install -U configparser python-slugify

cd /vagrant
sudo gem update --system
sudo gem install bundler
sudo npm install -g webpack
EOF

$user = <<EOF
# Purely optional & slow, sets up a dev environment
if [ ! -e ~/.my_scripts ]; then
  git clone --depth 1 https://github.com/starcraftman/.my_scripts/ ~/.my_scripts
  rm ~/.bashrc
  python .my_scripts/SysInstall.py home_save home
  sed --in-place -e "s/Plug 'Valloric.*//" ~/.vimrc
  echo "vim +Bootstrap +qa >/dev/null 2>&1"
  vim +Bootstrap +qa >/dev/null 2>&1
  echo "vim +PlugInstall +qa >/dev/null 2>&1"
  vim +PlugInstall +qa >/dev/null 2>&1
fi

echo "cd /vagramt && make >/dev/null 2>&1 &" >> ~/.lbashrc

cd /vagrant
bundle install
npm install
make &
sleep 5
make init_db
if [ -f rethinkdb_dump_2015-12-15.tar.gz ]; then
  rethinkdb restore --force -i vim_awesome ./rethinkdb_dump_2015-12-15.tar.gz
else
  echo "Save time, put dump in project root."
fi
EOF

Vagrant.require_version ">= 1.5.0"

VAGRANTFILE_API_VERSION = 2
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "boxcutter-VAGRANTSLASH-ubuntu1510"

  config.vm.provider :virtualbox do |v|
    # You may want to modify these if you don't use vagrant-faster
    #v.cpus = 4
    #v.memory = 4096
    v.customize ["modifyvm", :id, '--chipset', 'ich9'] # solves kernel panic issue on some host machines
    v.customize ["modifyvm", :id, "--ioapic", "on"]
  end

  if Vagrant.has_plugin?("vagrant-cachier")
    # Configure cached packages to be shared between instances of the same base box.
    # More info on http://fgrehm.viewdocs.io/vagrant-cachier/usage
    config.cache.scope = :box
  end

  config.vm.network :forwarded_port, guest: 5001, host: 5000
  config.vm.provision :shell, :inline => $root
  config.vm.provision :shell, :inline => $user, privileged: false
end
