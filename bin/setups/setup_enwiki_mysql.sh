#sudo apt-get -y install mysql-server

#mysql -p -e "\
#drop user 'alladmin'@'localhost';\
#flush privileges;"

#echo "create user 'alladmin'@'localhost'"
#mysql -p -e "\
#create user 'alladmin'@'localhost' identified by 'admin';\
#flush privileges;"

#drop database enwiki;\
echo "create database enwiki"
sudo mysql -p -e "\
create database enwiki;\
grant ALL on enwiki.* to 'alladmin'@'localhost';\
flush privileges;"

echo "create table enwiki.nodes"
sudo mysql -p -e "\
create table enwiki.nodes (\
id int, \
title text, \
sentence longtext, \
doc2vec text, \
tensorflow text, \
attribute tinytext, \
cluster tinytext, \
label tinytext, \
image text, \
color tinytext,\
timestamp datetime);\
alter table enwiki.nodes default character set "utf8mb4";\
flush privileges;"

echo "create table enwiki.edges"
sudo mysql -p -e "\
create table enwiki.edges (\
id int, \
start int, \
end int, \
relevancy float);\
flush privileges;"
