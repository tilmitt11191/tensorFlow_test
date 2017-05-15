#sudo apt-get -y install mysql-server

#sudo mysql -p -e "\
#drop user 'alladmin'@'localhost';\
#flush privileges;"

echo "create user 'alladmin'@'localhost'"
sudo mysql -p -e "\
create user 'alladmin'@'localhost' identified by 'admin';\
flush privileges;"

#drop database wikitext;\
echo "create database wikitext"
sudo mysql -p -e "\
create database wikitext;\
grant ALL on wikitext.* to 'alladmin'@'localhost';\
flush privileges;"

echo "create table wikitext.nodes"
sudo mysql -p -e "\
create table wikitext.nodes (\
id int, \
title text, \
vector text, \
attribute tinytext, \
label tinytext, \
image text, \
color tinytext,\
timestamp datetime);\
alter table wikitext.nodes default character set "utf8";\
flush privileges;"

echo "create table wikitext.edges"
sudo mysql -p -e "\
create table wikitext.edges (\
id int, \
start int, \
end int, \
relevancy float);\
flush privileges;"
