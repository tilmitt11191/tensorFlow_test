#! /usr/bin/bash -x

$HADOOP_HOME/sbin/hadoop-daemon.sh start namenode
$HADOOP_HOME/sbin/yarn-daemon.sh start resourcemanager
