# mount the disk.iso on the user/db/data dir
date >> /var/log/pgaas.log
mount /var/dbs/$1/$2/disk.iso /var/dbs/$1/$2/data 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log
echo $?