#! /usr/bin/bash -x

$HADOOP_HOME/sbin/hadoop-daemon.sh start datanode
$HADOOP_HOME/sbin/yarn-daemon.sh start nodemanager
$SPARK_HOME/sbin/start-slave.sh -c 7 -m 31G spark://Gemini:7077
