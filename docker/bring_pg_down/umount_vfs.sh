date >> /var/log/pgaas.log
umount /var/dbs/$1/$2/data 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log
echo $?