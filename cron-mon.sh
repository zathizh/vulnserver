export pid=$(pidof python vulnserver-python.py)
if [ -z $pid ];then
	python /bin/sh -c /home/cghost/Desktop/vulnserver/vulnserver-python.py &
fi
