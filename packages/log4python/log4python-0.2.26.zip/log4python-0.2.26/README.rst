# log4p
log for python like java log4j2

use config file [log4p.py], in the application root directory.

2018.08.16 add syslog, flume support
----------------------------------
App Example:
from log4p import log
TestLog = log(__name__)
TestLog.debug("Debug Log")
TestLog.info("Info Log")

out put like this:
2015-01-20 16:18:47,692 DEBUG [Thread-3] data.LogInsert (LogInsert.py:172) - Debug Log
2015-01-20 16:18:47,692 DEBUG [Thread-3] data.LogInsert (LogInsert.py:173) - Info Log

----------------------------------
Config Example:

config ={
    'monitorInterval' : 10,
    'loggers' :{
        'LogThread' :{
            'level': "DEBUG",
            'additivity' : False,
            'AppenderRef' : ['A1']
            },
        'root' :{
            #'level' : "CRITICAL",
            'level' : "ERROR",
            'AppenderRef' : ['output_root']
        }
    },

    'appenders' :{
        'output_root' :{
            'type' :"file",
            'FileName' :"root_error.log",
	    'backup_count': 5,
	    'file_size_limit': 1024 * 1024 * 20
            'PatternLayout' :"[level:%(levelname)s-file:%(filename)s-lineno:%(lineno)d] %(asctime)s %(message)s"
        },
        'A1' :{
            'type' :"file",
            'FileName' :"A2.log",
            'PatternLayout' :"[level:%(levelname)s-file:%(filename)s-lineno:%(lineno)d] %(asctime)s %(message)s"
        },
	'flumeTest' :{
            'type': "FLUME",
            'host': "192.168.10.120",
            'port': 44444,
            'headers': {'application': 'Skyline.Analyzer'},
            'PatternLayout': "[PID:%(process)d-level:%(levelname)s-file:%(filename)s-lineno:%(lineno)d] %(asctime)s %(message)s"
        },
        'console' :{
            'type' :"console",
            'target' :"console",
            'PatternLayout' :"[%(levelname)s] %(asctime)s %(message)s"
        }
    }
}


