FROM centos:latest
MAINTAINER Juan Luis Baptiste <jbaptiste@cachesimple.com>

RUN yum install -y epel-release
RUN yum update -y
RUN yum install -y bc curlftpfs fuse-curlftpfs git mailx python python-setuptools
# Make ssh dir and netstorage directories
RUN mkdir -p /root/.ssh/
# Copy over private key, and set permissions
ADD id_deploy_csi /root/.ssh/id_rsa
#ADD netstoragekit.json /root/.netstoragekit.json
RUN chmod -R 600 /root/.ssh && \
    touch /root/.ssh/known_hosts && \
# Add bitbuckets key
    ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts && \
# Clone the conf files into the docker container
    git clone git@bitbucket.org:jbaptiste_cs/cachesimple-scripts.git && \
    chmod 755 /cachesimple-scripts/netstorage/run_nsreport.sh && \
    chmod 755 /cachesimple-scripts/netstorage/new/netstorage_report.py && \
    easy_install pip && \
    pip install netstoragekit && \
    mkdir /reports
VOLUME ["/reports"]
CMD "/cachesimple-scripts/netstorage/new/netstorage_report.py"
