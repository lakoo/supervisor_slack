#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import slackweb
import os
from config import Config

f = file(os.path.join(os.path.dirname(__file__), 'conf/slack.cfg'))
cfg = Config(f)

slack = slackweb.Slack(url=cfg.slack_url)

def write_stdout(s):
    # only eventlistener protocol messages may be sent to stdout
    sys.stdout.write(s)
    sys.stdout.flush()

def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()

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
            attachments = []
            attachment = {"title": cfg.messages.start.title, "color": "warning", "text": cfg.messages.start.text}
            attachments.append(attachment)
            slack.notify(attachments=attachments)

        elif 'PROCESS_STATE_STARTED' == headers['eventname'] or 'PROCESS_STATE_RUNNING' == headers['eventname']:
            attachments = []
            attachment = {"title": cfg.messages.running.title, "color": "good", "text": cfg.messages.running.text}
            attachments.append(attachment)
            slack.notify(attachments=attachments)

        elif 'PROCESS_STATE_EXITED' == headers['eventname'] or 'PROCESS_STATE_STOPPED' == headers['eventname']:
            attachments = []
            attachment = {"title": cfg.messages.stop.title, "color": "danger", "text": cfg.messages.stop.text}
            attachments.append(attachment)
            slack.notify(attachments=attachments)

        elif 'PROCESS_STATE_FATAL' == headers['eventname']:
            attachments = []
            attachment = {"title": cfg.messages.fatal.title, "color": "danger", "text": cfg.messages.fatal.text}
            attachments.append(attachment)
            slack.notify(attachments=attachments)

        # transition from READY to ACKNOWLEDGED
        write_stdout('RESULT 2\nOK')

if __name__ == '__main__':
    main()