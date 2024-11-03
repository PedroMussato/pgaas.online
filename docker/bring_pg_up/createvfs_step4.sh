date >> /var/log/pgaas.log
echo "/var/dbs/$1/$2.iso /var/dbs/$1/$2/data ext4 defaults 0 0" >> /etc/fstab
echo $?