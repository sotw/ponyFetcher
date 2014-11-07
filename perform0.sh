synoindexPath='/usr/syno/bin/synoindex'
pythonPath='python'

function synoindex_update
{
	if [ -x $synoindexPath ]; then
		$synoindexPath -R $PWD/$1
	fi
}

function travelNode
{
	mkdir -p $1
	if [ -x $pythonPath ]; then
		$pythonPath ponyFetcherList.py $2 $1 0
	fi
}

bkIFS=$IFS
IFS=$'\r\n'
DATA=($(cat ./data))
for line in ${DATA[@]}
do
	IFS=' ' 
	read -a array <<< $line
	echo ${array[0]}
	echo ${array[1]}
	travelNode ${array[0]} ${array[1]}
	IFS=$'\r\n'
done
IFS=$bkIFS
