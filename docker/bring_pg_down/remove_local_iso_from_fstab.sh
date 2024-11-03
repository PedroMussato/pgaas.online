date >> /var/log/pgaas.log
sed -i "/\/var\/dbs\/$1\/$2.iso \/var\/dbs\/$1\/$2 ext4 defaults 0 0/d" /etc/fstab  1>> /var/log/pgaas.log 2>> /var/log/pgaas.log
echo $?