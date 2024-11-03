# create the user/db/data dir 
date >> /var/log/pgaas.log ; mkdir -p /var/dbs/$1/$2/data 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log ; echo $?
# create the disk.iso in the user/db dir 
date >> /var/log/pgaas.log ; dd if=/dev/zero of=/var/dbs/$1/$2/disk.iso bs=1M count=$3 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log ; echo $?
# make file system on user/db/disk.iso
date >> /var/log/pgaas.log ; mkfs -t ext4 /var/dbs/$1/$2/disk.iso 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log ; echo $?
# record on fstab the disk.iso to mount on the user/db/data dir
date >> /var/log/pgaas.log ; echo "/var/dbs/$1/$2/disk.iso /var/dbs/$1/$2/data ext4 defaults 0 0" >> /etc/fstab ; echo $?
# reload services
date >> /var/log/pgaas.log ; systemctl daemon-reload 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log ; echo $?
# mount the disk.iso on the user/db/data dir
date >> /var/log/pgaas.log ; mount /var/dbs/$1/$2/disk.iso /var/dbs/$1/$2/data 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log ; echo $?
# create docker compose file
echo "" > /var/dbs/$1/$2/pg_$1_$2.yaml ; echo "" >> /var/dbs/$1/$2/pg_$1_$2.yaml ; echo "services:" >> /var/dbs/$1/$2/pg_$1_$2.yaml ; echo "    pg.$1.$2:" >> /var/dbs/$1/$2/pg_$1_$2.yaml ; echo "        image: postgres:latest # Allow the client to specify the version" >> /var/dbs/$1/$2/pg_$1_$2.yaml ; echo "        restart: always" >> /var/dbs/$1/$2/pg_$1_$2.yaml ; echo "        ports:" >> /var/dbs/$1/$2/pg_$1_$2.yaml ; echo "            - $3:5432 # Use a random port for the client" >> /var/dbs/$1/$2/pg_$1_$2.yaml ; echo "        expose:" >> /var/dbs/$1/$2/pg_$1_$2.yaml ; echo "            - $3 # Use the same port internally" >> /var/dbs/$1/$2/pg_$1_$2.yaml ; echo "        environment:" >> /var/dbs/$1/$2/pg_$1_$2.yaml ; echo "            POSTGRES_PASSWORD: $4 # Generate a random password" >> /var/dbs/$1/$2/pg_$1_$2.yaml ; echo "        volumes:" >> /var/dbs/$1/$2/pg_$1_$2.yaml ; echo "            - /var/$1/$2/data:/var/lib/postgresql/data # Adjust path as needed" >> /var/dbs/$1/$2/pg_$1_$2.yaml ; echo "        deploy:" >> /var/dbs/$1/$2/pg_$1_$2.yaml ; echo "            resources:" >> /var/dbs/$1/$2/pg_$1_$2.yaml ; echo "                limits:" >> /var/dbs/$1/$2/pg_$1_$2.yaml ; echo "                    cpus: '$5' # Limit CPU usage (e.g., 0.5 cores)" >> /var/dbs/$1/$2/pg_$1_$2.yaml ; echo "                    memory: $6M # Limit RAM (e.g., 512 MB)" >> /var/dbs/$1/$2/pg_$1_$2.yaml ; echo "" >> /var/dbs/$1/$2/pg_$1_$2.yaml
# start container
date >> /var/log/pgaas.log ; docker compose -f /var/dbs/$1/$2/pg_$1_$2.yaml up -d 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log ; echo $?
