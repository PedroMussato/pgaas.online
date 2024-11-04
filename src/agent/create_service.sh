
# PAY ATTENTION ON THE
# !!!CHANGE HERE!!!!
# INTO THE CODE

echo '[Unit]' >> /etc/systemd/system/pgaas_agent.service
echo 'Description=Run pgaas agent as root' >> /etc/systemd/system/pgaas_agent.service
echo 'After=network.target' >> /etc/systemd/system/pgaas_agent.service
echo '' >> /etc/systemd/system/pgaas_agent.service
echo '[Service]' >> /etc/systemd/system/pgaas_agent.service
echo 'ExecStart=/usr/bin/python3 !!!CHANGE HERE!!!!' >> /etc/systemd/system/pgaas_agent.service
echo 'WorkingDirectory=!!!CHANGE HERE!!!!' >> /etc/systemd/system/pgaas_agent.service
echo 'Restart=on-failure' >> /etc/systemd/system/pgaas_agent.service
echo '' >> /etc/systemd/system/pgaas_agent.service
echo '[Install]' >> /etc/systemd/system/pgaas_agent.service
echo 'WantedBy=multi-user.target' >> /etc/systemd/system/pgaas_agent.service
echo '' >> /etc/systemd/system/pgaas_agent.service
systemctl daemon-reload
systemctl start pgaas_agent.service
systemctl enable pgaas_agent.service
sudo systemctl status mainpy.service
