# ColorLogging: A simple Python logger with colored log levels

[![GitHub version](https://badge.fury.io/gh/tjkessler%2FColorLogging.svg)](https://badge.fury.io/gh/tjkessler%2FColorLogging)
[![PyPI version](https://badge.fury.io/py/colorlogging.svg)](https://badge.fury.io/py/colorlogging)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/TJKessler/ColorLogging/master/LICENSE.txt)

## Installation:

### Prerequisites:
- Have Python 3.X installed
- Have the ability to install Python packages

### Method 1: pip
If your Python install contains pip:
```
pip install colorlogging
```
Note: if multiple Python releases are installed on your system (e.g. 2.7 and 3.6), you may need to execute the correct version of pip. For Python 3.X, change **pip install colorlogging** to **pip3 install colorlogging**.

### Method 2: From source
- Download the ColorLogging repository, navigate to the download location on the command line/terminal, and execute 
**"python setup.py install"**. 

## Usage

The simplest way to use the ColorLogger is with the "log" function:
```python
from colorlogging import log
log('debug', 'This is a debugging log!')
log('info', 'This is an information log!')
log('warn', 'This is a warning log!')
log('error', 'This is an error log!')
log('crit', 'This is a critical log!')
```

The "log" function accepts:
- level: log level for message
- message: message to log

with optional arguments:
- name: name of the logger
- log_dir: where to save the logs (defaults to "./logs")
- use_color: whether to log to the stream using color (defaults to True)

To work in a lower level with ColorLogging, import the ColorLogger with:
```python
from colorlogging import ColorLogger
```

And initialize it:
```python
my_logger = ColorLogger()
```

You can change the directory that logs are saved to when initializing:
```python
my_logger = ColorLogger(log_dir='path/to/my/log/directory')
```
By default, logs are saved to "/logs" in your current working directory.

ColorLogger will log Debugging, Information, Warning, Error and Critical messages. To change the minimum log level for stream logging and file logging, specify it in the initialization of the ColorLogger or by setting the value:
```python
my_logger = ColorLogger(stream_level='warn', file_level='info')
my_logger.stream_level = 'warn'
my_logger.file_level = 'info'
```
By default, ColorLogger will log everything to the console and to a log file.

Supported log levels (in argument form) are:
- 'debug' (debugging)
- 'info' (information)
- 'warn' (warning)
- 'error' (error)
- 'crit' (critical)
- 'disable' (turn off logging)

To log a message, supply your desired log level and a message:
```python
my_logger.log('warn', 'This is a warning message!')
```

Output stream format:

![Example run of code](Documentation/example_output.png)

Log records contain a timestamp, the function/line where the log occurred, a colored log level, and the supplied message. Log files are populated with logs in the same format, without coloring.

To turn off colors for stream logging, specify it in the initialization of your ColorLogger:
```python
my_logger = ColorLogger(use_color=False)
```

## Contributing, Reporting Issues and Other Support:

To contribute to ColorLogging, make a pull request. Contributions should include tests for new features added, as well as extensive documentation.

To report problems with the software or feature requests, file an issue. When reporting problems, include information such as error messages, your OS/environment and Python version.

For additional support/questions, contact Travis Kessler (travis.j.kessler@gmail.com).
