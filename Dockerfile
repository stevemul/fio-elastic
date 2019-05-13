FROM ubuntu:18.10
MAINTAINER Steve Mulholland

RUN apt-get -y update
RUN apt-get -y install fio \
   wget \
   python2.7 \
   python-pip

RUN pip install elasticsearch

# Check ENV vars
ADD check.sh /opt/check.sh
RUN chmod +x /opt/check.sh

# Copy in the script to push to elasticsearch
ADD elastic-push.py /opt/elastic-push.py
RUN chmod +x /opt/elastic-push.py

# Prepare to run the fio job
VOLUME /tmp/fio-data
ADD run.sh /opt/run.sh
RUN chmod +x /opt/run.sh
WORKDIR /tmp/fio-data

CMD ["/opt/run.sh"]
