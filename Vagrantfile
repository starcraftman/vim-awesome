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
apt-get update -y
apt-get dist-upgrade -y
apt-get autoremove -y
apt-get install -y \
    build-essential automake autopoint autoconf pkg-config cmake ninja ccache \
    git mercurial vim zip unzip unrar rar p7zip-full tree htop dfc \
    rethinkdb npm exuberant-ctags silversearcher-ag ack-grep \
    ruby ruby-dev python-dev pandoc sphinx-common \
    libyaml-dev libxml2-dev libxslt-dev zlib1g-dev \
    lubuntu-desktop
# lubuntu adds many packages, installs a small light gui you can use firefox from to see site

# Webpack expects node
ln -s /usr/bin/nodejs /usr/bin/node

curl -s https://bootstrap.pypa.io/get-pip.py > /tmp/get-pip.py
python /tmp/get-pip.py
pip install -U Flask Flask-Cache PyYAML html5lib lxml nose python-dateutil \
    requests rethinkdb termcolor configparser python-slugify

gem update --system
gem install bundler
npm install -g webpack
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

cd /vagrant
bundle install
npm install

echo "alias fstart='make -C /vagrant >/tmp/server.log 2>&1 &'" >> ~/.lbashrc
echo "alias flog='tail -n 50 /tmp/server.log" >> ~/.lbashrc
make -C /vagrant &
sleep 5
make init_db
if [ ! -f rethinkdb_dump_2015-12-15.tar.gz ]; then
  echo "Please wait while the database dump is downloaded to the project root."
  echo "Do not delete it and it will be reused should you need to provision anoter vagrant."
  curl -fLo rethinkdb_dump_2015-12-15.tar.gz https://dl.dropboxusercontent.com/u/18795947/rethinkdb_dump_2015-12-15.tar.gz
fi
rethinkdb restore --force -i vim_awesome ./rethinkdb_dump_2015-12-15.tar.gz
echo "Please execute on host: vagrant reload"
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
