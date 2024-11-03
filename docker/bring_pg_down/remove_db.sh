date >> /var/log/pgaas.log
rm -fr /var/dbs/$1 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log
echo $?
