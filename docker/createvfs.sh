mkdir -p /var/username/dbiid
dd if=/dev/zero of=/var/username/dbiid.iso bs=1M count=100
mkfs -t ext4 /var/username/dbiid.iso
mount /var/username/dbiid.iso /var/username/dbiid
