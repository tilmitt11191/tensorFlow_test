
# -*- coding: utf-8 -*-


#sudo apt-get -y install mysql-server

#sudo mysql -p -e "\
#drop user 'alladmin'@'localhost';\
#flush privileges;"

sudo mysql -p -e "\
create user 'alladmin'@'localhost' identified by 'admin';\
flush privileges;"

sudo mysql -p -e "\
create database mnist;\
grant ALL on mnist.* to 'alladmin'@'localhost';\
flush privileges;"

sudo mysql -p -e "\
create table mnist.tf_parameters (\
id int, \
v1 float, \
v2 float, \
v3 float, \
v4 float, \
v5 float, \
v6 float, \
v7 float, \
v8 float, \
v9 float, \
v0 float);\
flush privileges;"

sudo mysql -p -e "\
create table mnist.edges (\
id int, \
start int, \
end int, \
relevancy float);\
flush privileges;"

#id int NOT NULL PRIMARY KEY
