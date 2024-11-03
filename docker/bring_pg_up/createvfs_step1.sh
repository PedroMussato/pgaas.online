# create the user/db/data dir 
date >> /var/log/pgaas.log
mkdir -p /var/dbs/$1/$2/data 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log
echo $?