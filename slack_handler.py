#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import slackweb
import os
from config import Config
try:
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import HTTPError

f = file(os.path.join(os.path.dirname(__file__), 'conf/slack.cfg'))
cfg = Config(f)

slack = slackweb.Slack(url=cfg.slack_url)
if hasattr(cfg, 'slack_channel') and cfg.slack_channel != '':
    slack_channel=cfg.slack_channel if cfg.slack_channel[0] == '#' else '#' + cfg.slack_channel
else:
    slack_channel=''

def write_stdout(s):
    # only eventlistener protocol messages may be sent to stdout
    sys.stdout.write(s)
    sys.stdout.flush()

def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()

def notify(title, color, text):
    attachments = [{'title': title, 'color': color, 'text': text}]
    try:
        slack.notify(attachments=attachments, channel=slack_channel)
    except HTTPError as err:
        write_stderr(str(err))

def main():
    while 1:
        # transition from ACKNOWLEDGED to READY
        write_stdout('READY\n')

        # read header line and print it to stderr
        line = sys.stdin.readline()

        # read event payload and print it to stderr
        headers = dict([ x.split(':') for x in line.split() ])
        data = sys.stdin.read(int(headers['len']))
        if 'PROCESS_STATE_STARTING' == headers['eventname']:
            notify(cfg.messages.start.title, 'warning', cfg.messages.start.text)

        elif 'PROCESS_STATE_STARTED' == headers['eventname'] or 'PROCESS_STATE_RUNNING' == headers['eventname']:
            notify(cfg.messages.running.title, 'good', cfg.messages.running.text)

        elif 'PROCESS_STATE_EXITED' == headers['eventname'] or 'PROCESS_STATE_STOPPED' == headers['eventname']:
            notify(cfg.messages.stop.title, 'danger', cfg.messages.stop.text)

        elif 'PROCESS_STATE_FATAL' == headers['eventname']:
            notify(cfg.messages.fatal.title, 'danger', cfg.messages.fatal.text)

        # transition from READY to ACKNOWLEDGED
        write_stdout('RESULT 2\nOK')

if __name__ == '__main__':
    main()