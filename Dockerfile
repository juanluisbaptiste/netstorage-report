FROM centos:latest
MAINTAINER Juan Luis Baptiste <jbaptiste@cachesimple.com>

# Copy over private key
ADD id_deploy_csi /root/.ssh/id_rsa

RUN yum install -y epel-release && \
    yum update -y && \
    yum install -y bc cronie curlftpfs fuse-curlftpfs git mailx python python-setuptools ssh && \
    mkdir -p /root/.ssh/ && \
    chmod -R 600 /root/.ssh && \
    touch /root/.ssh/known_hosts && \
    ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts && \
# Clone the conf files into the docker container
    git clone git@bitbucket.org:jbaptiste_cs/cachesimple-scripts.git && \
    chmod 755 /cachesimple-scripts/netstorage/run_nsreport.sh && \
    chmod 755 /cachesimple-scripts/netstorage/new/netstorage_report.py && \
    easy_install pip && \
    pip install netstoragekit && \
    ln -sf /dev/stdout /var/log/cron.log && \
ADD *.sh /
RUN chmod 755 /start.sh && \
    chmod 755 /run.sh
#ADD netstoragekit.json /root/.netstoragekit.json

VOLUME ["/reports"]
#CMD "/cachesimple-scripts/netstorage/new/netstorage_report.py"
CMD "/start.sh"
