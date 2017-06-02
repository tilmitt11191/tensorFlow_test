#!/bin/bash

MASTER_USERNAME="ozu"
MASTER_HOSTNAME="Gemini"
declare -A ACCOUNTS
ACCOUNTS=( \
	["172.19.73.73"]="ozu" \
	["172.19.73.160"]="alladmin" \
)
declare -A SSHPORTS
SSHPORTS=( \
	["172.19.73.73"]=22 \
	["172.19.73.160"]=22 \
)

line=`cat $HADOOP_HOME/logs/hadoop-$MASTER_USERNAME-namenode-$MASTER_HOSTNAME.log |\
	grep -E application_[0-9]*_[0-9]* | tail -n 1`
if [[ "$line" =~ application_[0-9]*_[0-9]* ]]; then
	APPLICATION_ID=${BASH_REMATCH[0]}
fi

DATANODE_LOGDIR=$HADOOP_HOME/logs/userlogs/$APPLICATION_ID/
LOGDIR="$HOME/print_spark_logdir"
LOGFILE=$LOGDIR/all-$APPLICATION_ID""
echo "####"$APPLICATION_ID"####" > $LOGFILE

if [ ! -e $LOGDIR ]; then
	mkdir $LOGDIR
fi

function get_logs () {
	ipaddress=$1
	account=$2
	port=$3
	hostname=`ssh $account"@"$ipaddress -p $port hostname`

	scp -P $port -r $account"@"$ipaddress:$DATANODE_LOGDIR $LOGDIR >/dev/null 2>&1

	dirs="$LOGDIR/$APPLICATION_ID/*"
	for dir in $dirs; do
		if [ -d $dir ]; then
			echo "########"$hostname:$dir"########" >> $LOGFILE
			files="$dir/*"
			for file in $files; do
				echo "############"$hostname:$file"############" >> $LOGFILE

				cat $file >> $LOGFILE
			done
		fi
	done
}

for IPADDRESS in ${!ACCOUNTS[@]}; do
	get_logs $IPADDRESS ${ACCOUNTS[$IPADDRESS]} ${SSHPORTS[$IPADDRESS]}
done

cat $LOGFILE
exit 0
