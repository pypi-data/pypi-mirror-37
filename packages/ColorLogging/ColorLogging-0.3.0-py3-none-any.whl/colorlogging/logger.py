#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  colorlogging/logger.py
#  v.0.3.0
#  Developed in 2018 by Travis Kessler <travis.j.kessler@gmail.com>
#
#  A simple Python logger with colored log levels
#

# Python stdlib imports
from inspect import currentframe, getframeinfo
import logging
import time
import copy
import os

# 3rd party imports
import colorama

# Log format (for stream output and file content)
LOG_FORMAT = '[%(asctime)s] [%(call_loc)s] [%(levelname)s] %(message)s'

# File format (timestamp.log)
FILE_FORMAT = '{}.log'.format(str(time.time()).split('.')[0])

# Colorama colors for log levels
COLORS = {
    logging.DEBUG: colorama.Fore.GREEN,
    logging.INFO: colorama.Fore.CYAN,
    logging.WARN: colorama.Fore.YELLOW,
    logging.ERROR: colorama.Fore.RED,
    logging.CRITICAL: colorama.Fore.LIGHTRED_EX
}


class ColorFormatter(logging.Formatter):
    '''
    Logging formatter for coloring log level in output stream
    '''

    def format(self, record, *args, **kwargs):
        if record.levelno not in COLORS.keys():
            raise ValueError(
                '{} not available for coloring'.format(record.levelname)
            )
        record_n = copy.copy(record)
        record_n.levelname = '{}{}{}'.format(
            COLORS[record_n.levelno],
            record_n.levelname,
            colorama.Style.RESET_ALL
        )
        return super(ColorFormatter, self).format(record_n, *args, **kwargs)


class ColorLogger:
    '''
    Color logger: colors log levels in output stream
    '''

    def __init__(self, log_dir='logs', stream_level='debug',
                 file_level='debug', use_color=True, name='color_logger'):
        '''
        *log_dir*       -   name of directory to save logs
        *file_level*    -   minimum level to save (default == 'debug')
        *stream_level*  -   minimum level to stream (default == 'debug')
        *use_color*     -   True == use color formatting, False == don't
        '''

        colorama.init()

        # If a ColorLogger already exists, get it. Otherwise, create one.
        self.__stream_logger = logging.getLogger(name + '_stream')
        self.__file_logger = logging.getLogger(name + '_file')

        if len(self.__stream_logger.handlers) == 0 and \
           len(self.__file_logger.handlers) == 0:

            s_handler = logging.StreamHandler()
            if use_color:
                s_handler.setFormatter(ColorFormatter(LOG_FORMAT, '%H:%M:%S'))
            else:
                s_handler.setFormatter(
                    logging.Formatter(LOG_FORMAT, '%H:%M:%S')
                )

            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            f_handler = logging.FileHandler(os.path.join(log_dir, FILE_FORMAT))
            f_handler.setFormatter(logging.Formatter(LOG_FORMAT, '%H:%M:%S'))

            self.__stream_logger = logging.Logger(name + '_stream')
            self.__stream_logger.addHandler(s_handler)
            self.__file_logger = logging.Logger(name + '_file')
            self.__file_logger.addHandler(f_handler)

        self.__levels = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warn': logging.WARN,
            'error': logging.ERROR,
            'crit': logging.CRITICAL,
            'disable': None
        }

        self.__log_fns = {
            'debug': (
                self.__file_logger.debug,
                self.__stream_logger.debug
            ),
            'info': (
                self.__file_logger.info,
                self.__stream_logger.info
            ),
            'warn': (
                self.__file_logger.warning,
                self.__stream_logger.warning
            ),
            'error': (
                self.__file_logger.error,
                self.__stream_logger.error
            ),
            'crit': (
                self.__file_logger.critical,
                self.__stream_logger.critical
            )
        }

        self.stream_level = stream_level
        self.file_level = file_level

    @property
    def stream_level(self):
        '''
        Returns current level of stream logger
        '''

        return self.__file_logger.getEffectiveLevel()

    @stream_level.setter
    def stream_level(self, level):
        '''
        Set stream logger level
        '''

        if level not in self.__levels.keys():
            raise ValueError('{} is not a valid log level'.format(level))
        if level == 'disable':
            self.__stream_logger.disabled = True
        else:
            self.__stream_logger.disabled = False
            self.__stream_logger.setLevel(self.__levels[level])

    @property
    def file_level(self):
        '''
        Returns current level of file logger
        '''

        return self.__file_logger.getEffectiveLevel()

    @file_level.setter
    def file_level(self, level):
        '''
        Set file logger level
        '''

        if level not in self.__levels.keys():
            raise ValueError('{} is not a valid log level'.format(level))
        if level == 'disable':
            self.__file_logger.disabled = True
        else:
            self.__file_logger.disabled = False
            self.__file_logger.setLevel(self.__levels[level])

    def log(self, level, message, call_loc=None):
        '''
        Log a *message* at log level *level*
        '''

        if level not in self.__log_fns.keys():
            raise ValueError('{} not a valid logging level'.format(level))

        if call_loc is None:
            call_loc = {'call_loc': '{}:{}'.format(
                getframeinfo(currentframe().f_back).function,
                getframeinfo(currentframe().f_back).lineno
            )}

        self.__log_fns[level][0](message, extra=call_loc)
        self.__log_fns[level][1](message, extra=call_loc)


def log(level, message, name='color_logger', log_dir='logs', use_color=True):
    '''
    Simple logging: logs *message* at log level *level*
    '''

    call_loc = {'call_loc': '{}:{}'.format(
        getframeinfo(currentframe().f_back).function,
        getframeinfo(currentframe().f_back).lineno
    )}
    logger = ColorLogger(log_dir=log_dir, name=name, use_color=use_color)
    logger.log(level, message, call_loc=call_loc)
