#!/bin/bash

echo "SMTP_TO=$SMTP_TO" >> /root/vars.env
echo "REMOTEPATH=$REMOTEPATH" >> /root/vars.env
echo "${CRONJOB_TIME} root /run.sh > /var/log/cron.log 2>&1" > /etc/cron.d/netstorage

crond
while true
do
  sleep 1000
done
