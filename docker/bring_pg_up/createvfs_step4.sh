# record on fstab the disk.iso to mount on the user/db/data dir
date >> /var/log/pgaas.log
echo "/var/dbs/$1/$2/disk.iso /var/dbs/$1/$2/data ext4 defaults 0 0" >> /etc/fstab
echo $?