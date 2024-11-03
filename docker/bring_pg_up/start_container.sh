# start container
date >> /var/log/pgaas.log
docker compose -f /var/dbs/$1/$2/pg_$1_$2.yaml up -d 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log
echo $?