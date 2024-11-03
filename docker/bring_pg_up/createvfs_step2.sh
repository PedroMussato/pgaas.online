date >> /var/log/pgaas.log
dd if=/dev/zero of=/var/dbs/$1/$2.iso bs=1M count=$3 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log
echo $?