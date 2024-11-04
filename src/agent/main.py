import requests
import json
import sqlite3
import time
import os
import datetime

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
        cursor.execute("select id, task, status, task_order, userid, dbiid from tasks where not status = 'done' ORDER BY id LIMIT 1 ;")
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
    
def inform_creation(userid, dbiid):
    data = dict()
    data[f'{userid}-{dbiid}'] = 'created'
    response = requests.post(SERVER + ENDPOINT, json=data)
    if response.status_code != 200:
        with open('response_again.data', 'a+') as file:
            file.write(f'https://{SERVER}{ENDPOINT},{userid},{dbiid},created\n')


def inform_deletion(userid, dbiid):
    data = dict()
    data[f'{userid}-{dbiid}'] = 'deleted'
    response = requests.post(SERVER + ENDPOINT, json=data)
    if response.status_code != 200:
        with open('response_again.data', 'a+') as file:
            file.write(f'https://{SERVER}{ENDPOINT},{userid},{dbiid},deleted\n')

create_db()

KEY = '7d6fb54a-7c2b-41dd-9d75-44fb3f668ac6'
SERVER = 'http://localhost:8000/'
ENDPOINT = f'agent_communication/{KEY}/'

with open('response_again.data', 'a+') as file:
    pass

while True:
    # check local db for not finished taks
    while True:
        tasks = get_next_task()
        if tasks:
            id = tasks[0][0]
            task = tasks[0][1]
            status = tasks[0][2]
            task_order = tasks[0][3]
            userid = tasks[0][4]
            dbiid = tasks[0][5]

            # log executions
            with open('tasks_executed.data', 'a+') as task_data_file:
                task_data_file.write(f'\n\n#{datetime.datetime.now()}\n{task}\n')

            # execute tasks # Run the command and get a file-like object
            with os.popen(task) as process:
                for line in process:
                    print(line.strip())  # Process each line of output as it comes
            if status == 'todo-create' and task_order == 8:
                inform_creation(userid, dbiid)
            elif status == 'todo-delete' and task_order == 4:
                inform_deletion(userid, dbiid)
            mark_task_as_done(id)
        else:
            break

    with open('response_again.data', 'r') as file:
        lines = file.read().split('\n')

    for line in lines:
        if line:
            linearr = line.split(',')
            data = dict()
            data[f'{linearr[1]}-{linearr[2]}'] = linearr[3]
            response = requests.post(linearr[0], json=data)
            if response.status_code == 200:
                lines.remove(line)

            with open('response_again.data', 'w') as file:
                for line in lines:
                    file.write(line+'\n')

    # make a request to get taks
    try:
        response = requests.get(SERVER + ENDPOINT)
    except:
        pass
    else:
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


    time.sleep(10)
