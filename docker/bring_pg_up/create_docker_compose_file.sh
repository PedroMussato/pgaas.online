echo "" > /var/dbs/$1/$2/pg_$1_$2.yaml
#echo "version: '3.9'" >> /var/dbs/$1/$2/pg_$1_$2.yaml
echo "" >> /var/dbs/$1/$2/pg_$1_$2.yaml
echo "services:" >> /var/dbs/$1/$2/pg_$1_$2.yaml
echo "    pg.$1.$2:" >> /var/dbs/$1/$2/pg_$1_$2.yaml
echo "        image: postgres:latest # Allow the client to specify the version" >> /var/dbs/$1/$2/pg_$1_$2.yaml
echo "        restart: always" >> /var/dbs/$1/$2/pg_$1_$2.yaml
echo "        ports:" >> /var/dbs/$1/$2/pg_$1_$2.yaml
echo "            - $3:5432 # Use a random port for the client" >> /var/dbs/$1/$2/pg_$1_$2.yaml
echo "        expose:" >> /var/dbs/$1/$2/pg_$1_$2.yaml
echo "            - $3 # Use the same port internally" >> /var/dbs/$1/$2/pg_$1_$2.yaml
echo "        environment:" >> /var/dbs/$1/$2/pg_$1_$2.yaml
echo "            POSTGRES_PASSWORD: $4 # Generate a random password" >> /var/dbs/$1/$2/pg_$1_$2.yaml
echo "        volumes:" >> /var/dbs/$1/$2/pg_$1_$2.yaml
echo "            - /var/$1/$2/data:/var/lib/postgresql/data # Adjust path as needed" >> /var/dbs/$1/$2/pg_$1_$2.yaml
echo "        deploy:" >> /var/dbs/$1/$2/pg_$1_$2.yaml
echo "            resources:" >> /var/dbs/$1/$2/pg_$1_$2.yaml
echo "                limits:" >> /var/dbs/$1/$2/pg_$1_$2.yaml
echo "                    cpus: '$5' # Limit CPU usage (e.g., 0.5 cores)" >> /var/dbs/$1/$2/pg_$1_$2.yaml
echo "                    memory: $6M # Limit RAM (e.g., 512 MB)" >> /var/dbs/$1/$2/pg_$1_$2.yaml
echo "" >> /var/dbs/$1/$2/pg_$1_$2.yaml
