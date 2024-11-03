date >> /var/log/pgaas.log
mount /var/dbs/$1/$2.iso /var/dbs/$1/$2/data 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log
echo $?