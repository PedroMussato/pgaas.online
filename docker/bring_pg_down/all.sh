#USERID = $1
#DBIID = $2

./stop_container.sh $1 $2
./remove_local_iso_from_fstab.sh $1 $2
./umount_vfs.sh $1 $2
./remove_db.sh $1 $2