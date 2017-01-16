#!/bin/bash

echo "SMTP_TO=$SMTP_TO" >> /root/vars.env
echo "REMOTEPATH=$REMOTEPATH" >> /root/vars.env

crond
while true
do
  sleep 1000
done
