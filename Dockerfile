FROM centos:7
MAINTAINER Juan Luis Baptiste <jbaptiste@cachesimple.com>
ENV CRONJOB_TIME "1 12 1 * *"

COPY netstorage_report.py /
RUN yum install -y epel-release && \
    yum update -y && \
    yum install -y bc cronie curlftpfs fuse-curlftpfs mailx python python-setuptools ssh && \
    chmod 755 /netstorage_report.py && \
    easy_install pip==20.3.4 && \
    pip install netstoragekit && \
    ln -sf /dev/stdout /var/log/cron.log && \
    echo "${CRONJOB_TIME} root /run.sh > /var/log/cron.log 2>&1" > /etc/cron.d/netstorage && \
    chmod 644 /etc/cron.d/netstorage
ADD start.sh /
ADD run.sh /
RUN chmod 755 /*.sh
#ADD netstoragekit.json /root/.netstoragekit.json

VOLUME ["/reports"]
CMD "/start.sh"
