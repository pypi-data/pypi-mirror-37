# -*- coding:utf-8 -*-

"""
Datadog logs logging handler and utilities
"""

__author__ = "Masashi Terui <marcy9114+pypi@gmail.com>"
__status__ = "beta"
__version__ = "0.1.1"
__date__    = "10 Oct 2018"


import json
import os
import logging
import socket
import ssl


class DatadogLogsHandler(logging.Handler):
    """
    Datadog logs logging handler
    """

    def __init__(self, *args, **kwargs):
        super(DatadogLogsHandler, self).__init__(
            level=kwargs.pop('level', logging.NOTSET))
        self.sourcecategory = kwargs.pop('source_category', 'ddlogs')
        self.source = kwargs.pop('source', 'python')
        self.service = kwargs.pop('service', None)
        self.host = kwargs.pop('host', socket.gethostname())
        self.api_key = kwargs.pop('api_key', os.environ.get('DD_API_KEY', ''))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 10514
        if kwargs.pop('ssl', True):
            self.socket = ssl.wrap_socket(self.socket)
            port = 10516
        self.socket.connect(('lambda-intake.logs.datadoghq.com', port))


    def emit(self, record):
        try:
            log = self.format(record)
            if isinstance(log, str): 
                log =  {'message': log}
            elif not isinstance(log, dict):
                raise Exception(
                    'Cannot send the entry as it must be either a string or a dict.'
                    + 'Provided entry: '
                    + str(log)
                )
            status = 'info'
            if record.levelno >= logging.ERROR:
                status = 'error'
            elif record.levelno == logging.WARNING:
                status = 'warning'
            service = self.service
            if service is None:
                service = record.name
            log.update({
                'ddsourcecategory': self.sourcecategory,
                'ddsource': self.source,
                'service': service,
                'host': self.host,
                'status': status})
            self.socket.send('{} {}\n'.format(
                self.api_key,
                json.dumps(log)).encode('utf-8'))
        except:
            self.handleError(record)


class DictFormatter(logging.Formatter):
    """
    Simple dict formatter for Datadog logs logging handler
    """

    def format(self, record):
        ret = {}
        for attr, value in record.__dict__.items():
            if attr == 'asctime':
                value = self.formatTime(record)
            if attr == 'exc_info' and value is not None:
                value = self.formatException(value)
            if attr == 'stack_info' and value is not None:
                value = self.formatStack(value)
            ret[attr] = value
        return ret
