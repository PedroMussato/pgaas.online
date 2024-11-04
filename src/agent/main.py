import requests
import json
import sqlite3
import time
import os

def create_db():
    with sqlite3.connect('agent.sqlite3') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                userid INTEGER,
                dbiid INTEGER,
                task_order INTEGER,
                task TEXT,
                status TEXT,
                UNIQUE (userid, dbiid, task)
            );
        ''')
        conn.commit()

def insert_task(userid, dbiid, task_order, task, status):
    with sqlite3.connect('agent.sqlite3') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (userid, dbiid, task_order, task, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (userid, dbiid, task_order, task, status))
        conn.commit()

def get_next_task():
    with sqlite3.connect('agent.sqlite3') as conn:
        cursor = conn.cursor()
        cursor.execute("select id, task from tasks where not status = 'done' ORDER BY id LIMIT 1 ;")
        rows = cursor.fetchall()
        return rows

def mark_task_as_done(id):
    with sqlite3.connect('agent.sqlite3') as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
            UPDATE tasks
            SET status = 'done'
            WHERE id = {id}
        ''')
        conn.commit()
    
create_db()

KEY = '7d6fb54a-7c2b-41dd-9d75-44fb3f668ac6'
SERVER = 'http://localhost:8000/'
ENDPOINT = f'agent_communication/{KEY}/'

while True:
    # check local db for not finished taks
    tasks = get_next_task()
    if tasks:
        id = tasks[0][0]
        task = tasks[0][1]
        # execute tasks
        # Run the command and get a file-like object
        with os.popen(task) as process:
            for line in process:
                print(line.strip())  # Process each line of output as it comes
        mark_task_as_done(id)


        ## when executed, return to server the status

    # make a request to get taks
    response = requests.get(SERVER + ENDPOINT)

    # Check if the response is successful
    if response.status_code == 200:
        # Process the response
        data = response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")

    for k in data.keys():
        userid = data[k]['userid']
        dbiid = data[k]['dbiid']
        password = data[k]['password']
        cpu = data[k]['cpu']
        ram = data[k]['ram']
        disk = data[k]['disk']
        port = data[k]['port']
        status = data[k]['status']

        if status == 'on-creation':
            # create the user/db/data dir 
            task1 = \
f"""
date >> /var/log/pgaas.log
mkdir -p /var/dbs/{userid}/{dbiid}/data 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log
echo $?
"""
            try:
                insert_task(userid, dbiid, 1, task1, 'todo-create')
            except: 
                pass

            # create the disk.iso in the user/db dir 
            task2 = \
f"""
date >> /var/log/pgaas.log
dd if=/dev/zero of=/var/dbs/{userid}/{dbiid}/disk.iso bs=1M count={disk} 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log
echo $?
"""
            try:
                insert_task(userid, dbiid, 2, task2, 'todo-create')
            except: 
                pass


            # make file system on user/db/disk.iso
            task3 = \
f"""
date >> /var/log/pgaas.log
mkfs -t ext4 /var/dbs/{userid}/{dbiid}/disk.iso 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log
echo $?
"""
            try:
                insert_task(userid, dbiid, 3, task3, 'todo-create')
            except: 
                pass


            # record on fstab the disk.iso to mount on the user/db/data dir
            task4 = \
f"""
date >> /var/log/pgaas.log
echo "/var/dbs/{userid}/{dbiid}/disk.iso /var/dbs/{userid}/{dbiid}/data ext4 defaults 0 0" >> /etc/fstab
echo $?
"""
            try:
                insert_task(userid, dbiid, 4, task4, 'todo-create')
            except: 
                pass


            # reload services
            task5 = \
f"""
date >> /var/log/pgaas.log
systemctl daemon-reload 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log
echo $?
"""
            try:
                insert_task(userid, dbiid, 5, task5, 'todo-create')
            except: 
                pass


            # mount the disk.iso on the user/db/data dir
            task6 = \
f"""
date >> /var/log/pgaas.log
mount /var/dbs/{userid}/{dbiid}/disk.iso /var/dbs/{userid}/{dbiid}/data 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log
echo $?
"""
            try:
                insert_task(userid, dbiid, 6, task6, 'todo-create')
            except: 
                pass


            # create docker compose file
            task7 = \
f"""
echo "" > /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
#echo "version: '3.9'" >> /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
echo "" >> /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
echo "services:" >> /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
echo "    pg.{userid}.{dbiid}:" >> /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
echo "        image: postgres:latest # Allow the client to specify the version" >> /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
echo "        restart: always" >> /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
echo "        ports:" >> /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
echo "            - {port}:5432 # Use a random port for the client" >> /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
echo "        expose:" >> /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
echo "            - {port} # Use the same port internally" >> /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
echo "        environment:" >> /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
echo "            POSTGRES_PASSWORD: {password} # Generate a random password" >> /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
echo "        volumes:" >> /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
echo "            - /var/{userid}/{dbiid}/data:/var/lib/postgresql/data # Adjust path as needed" >> /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
echo "        deploy:" >> /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
echo "            resources:" >> /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
echo "                limits:" >> /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
echo "                    cpus: '{cpu}' # Limit CPU usage (e.g., 0.5 cores)" >> /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
echo "                    memory: {ram}M # Limit RAM (e.g., 512 MB)" >> /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
echo "" >> /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml
"""
            try:
                insert_task(userid, dbiid, 7, task7, 'todo-create')
            except: 
                pass


            # start container
            task8 = \
f"""
date >> /var/log/pgaas.log
docker compose -f /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml up -d 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log
echo $?
"""
            try:
                insert_task(userid, dbiid, 8, task8, 'todo-create')
            except: 
                pass


        elif status == 'on-deletion':
            task1 = \
f"""
date >> /var/log/pgaas.log
docker compose -f /var/dbs/{userid}/{dbiid}/pg_{userid}_{dbiid}.yaml down 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log
echo $?
"""
            try:
                insert_task(userid, dbiid, 1, task1, 'todo-delete')
            except: 
                pass

            task2 = \
f"""
date >> /var/log/pgaas.log
sed -i "/\/var\/dbs\/{userid}\/{dbiid}\/disk.iso \/var\/dbs\/{userid}\/{dbiid}\/data ext4 defaults 0 0/d" /etc/fstab  1>> /var/log/pgaas.log 2>> /var/log/pgaas.log
echo $?
"""
            try:
                insert_task(userid, dbiid, 2, task2, 'todo-delete')
            except: 
                pass

            task3 = \
f"""
date >> /var/log/pgaas.log
umount /var/dbs/{userid}/{dbiid}/data 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log
echo $?
"""
            try:
                insert_task(userid, dbiid, 3, task3, 'todo-delete')
            except: 
                pass

            task4 = \
f"""
date >> /var/log/pgaas.log
rm -fr /var/dbs/{userid}/{dbiid} 1>> /var/log/pgaas.log 2>> /var/log/pgaas.log
echo $?
"""
            try:
                insert_task(userid, dbiid, 4, task4, 'todo-delete')
            except: 
                pass


#    time.sleep(60)


