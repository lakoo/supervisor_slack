FROM python:2.7-slim-stretch
RUN mkdir /supervisor-slack
WORKDIR /supervisor-slack
COPY requirements.txt /supervisor-slack/
RUN pip install -r requirements.txt
COPY . /supervisor-slack
CMD [ "supervisord", "-n", "-c", "conf/supervisord.conf" ]
