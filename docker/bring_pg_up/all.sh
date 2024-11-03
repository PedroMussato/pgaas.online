# USERID = $1
# DBIID = $2
# SIZE = $3
# PORT = $4
# PASS = $5
# CPU = $6
# RAM = $7

./createvfs.sh $1 $2 $3
./create_docker_compose_file.sh $1 $2 $4 $5 $6 $7
./start_container.sh $1 $2
