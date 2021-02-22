FROM python:3.7-alpine
COPY bots/* /bots/

COPY requirements.txt /tmp
RUN apk add --no-cache bash
RUN pip3 install -r /tmp/requirements.txt
RUN chmod a+x /bots/run.sh

#WORKDIR /bots/
#CMD ["cat","run.sh"]
#CMD ["ls"]
CMD ["/bots/run.sh"]
