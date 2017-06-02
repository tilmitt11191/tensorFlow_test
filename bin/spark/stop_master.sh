
$SPARK_HOME/sbin/stop-master.sh
$HADOOP_HOME/sbin/hadoop-daemon.sh stop namenode
$HADOOP_HOME/sbin/yarn-daemon.sh stop resourcemanager

$HADOOP_HOME/sbin/stop-dfs.sh
