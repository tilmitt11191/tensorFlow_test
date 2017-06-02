#! /usr/bin/bash -x

$SPARK_HOME/sbin/stop-slave.sh
$HADOOP_HOME/sbin/hadoop-daemon.sh stop datanode
$HADOOP_HOME/sbin/yarn-daemon.sh stop nodemanager
