FROM centos:latest
MAINTAINER Juan Luis Baptiste <jbaptiste@cachesimple.com>

RUN yum install -y epel-release
RUN yum update -y
RUN yum install -y bc curlftpfs fuse-curlftpfs git mailx
# Make ssh dir and netstorage directories
RUN mkdir -p /root/.ssh/ && \
    mkdir -p /var/lib/akamai/netstorage/{remote,reports}
# Copy over private key, and set permissions
ADD id_deploy_csi /root/.ssh/id_rsa
RUN chmod -R 600 /root/.ssh 
# Create known_hosts
RUN touch /root/.ssh/known_hosts
# Add bitbuckets key
RUN ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts

# Clone the conf files into the docker container
RUN git clone git@bitbucket.org:jbaptiste_cs/cachesimple-scripts.git
RUN chmod 755 /cachesimple-scripts/netstorage/run_nsreport.sh

WORKDIR /cachesimple-scripts/netstorage/
VOLUME ["/var/lib/akamai"]
#CMD ["./reporteNS.sh", "-l", "-r", "35985/", "-d", "/var/lib/akamai/netstorage/remote"]
CMD ["./run_nsreport.sh"]
