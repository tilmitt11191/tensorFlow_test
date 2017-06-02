#! /usr/bin/bash -x

#$HADOOP_HOME/bin/hdfs namenode -format -clusterId  CID-a07eb260-9b6e-4f03-ad01-b21ca6c8c02d
$HADOOP_HOME/bin/hdfs namenode -format
$HADOOP_HOME/sbin/start-dfs.sh

$HADOOP_HOME/sbin/hadoop-daemon.sh start namenode
$HADOOP_HOME/sbin/yarn-daemon.sh start resourcemanager
$SPARK_HOME/sbin/start-master.sh
