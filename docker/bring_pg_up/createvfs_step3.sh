date >> /var/log/pgaas.log
mkfs -t ext4 /var/dbs/$1/$2.iso 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log
echo $?