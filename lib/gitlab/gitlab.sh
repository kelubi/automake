#!/bin/bash
#https://github.com/gitlabhq/gitlabhq/blob/master/doc/install/installation.md
#https://gist.github.com/toreym/3548041
#关键是要把gem和bundle的源改成淘宝的，其他的根据官方的搞就行


/usr/sbin/adduser --disabled-login --gecos 'GitLab'  git

gem sources --remove https://rubygems.org/
gem sources -a http://ruby.taobao.org/
gem sources -l
gem install rails passenger rake bundler grit --no-rdoc --no-ri

pip install pygments


gem install nokogiri -v '1.5.10'
gem install charlock_holmes -v '0.6.9.4'

yum install -y libxslt libxslt-devel

 
wget http://download.icu-project.org/files/icu4c/51.2/icu4c-51_2-src.tgz
tar xf icu4c-51_2-src.tgz
cd icu
cd source/
./configure --prefix=/usr
make
make install


cd /home/git/gitlab
su git
# Copy the example GitLab config
cp config/gitlab.yml.example config/gitlab.yml

# Make sure to change "localhost" to the fully-qualified domain name of your
# host serving GitLab where necessary
editor config/gitlab.yml

# Make sure GitLab can write to the log/ and tmp/ directories
sudo chown -R git log/
sudo chown -R git tmp/
sudo chmod -R u+rwX  log/
sudo chmod -R u+rwX  tmp/

# Create directory for satellites
mkdir /home/git/gitlab-satellites

# Create directories for sockets/pids and make sure GitLab can write to them
mkdir tmp/pids/
mkdir tmp/sockets/
chmod -R u+rwX  tmp/pids/
chmod -R u+rwX  tmp/sockets/

# Create public/uploads directory otherwise backup will fail
mkdir public/uploads
chmod -R u+rwX  public/uploads

# Copy the example Unicorn config
#cp config/unicorn.rb.example config/unicorn.rb
#这个和官方的不一样
cp config/puma.rb.example config/puma.rb


# Enable cluster mode if you expect to have a high load instance
# Ex. change amount of workers to 3 for 2GB RAM server
editor config/unicorn.rb

# Configure Git global settings for git user, useful when editing via web
# Edit user.email according to what is set in gitlab.yml
git config --global user.name "GitLab"
git config --global user.email "gitlab@localhost"
git config --global core.autocrlf input

sed -i 's,https://rubygems.org,http://ruby.taobao.org,g' Gemfile
bundle install --deployment --without development test postgres unicorn aws
rake db:setup RAILS_ENV=production
rake db:seed_fu RAILS_ENV=production

exit

cp /home/git/gitlab/lib/support/init.d/gitlab /etc/init.d/gitlab
chmod +x /etc/init.d/gitlab
chkconfig gitlab on

/etc/init.d/gitlab start
/etc/init.d/redis start
