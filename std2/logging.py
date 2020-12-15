from logging import (DEBUG, ERROR, FATAL, INFO, WARN, FileHandler, Formatter,
                     Handler, LogRecord, StreamHandler, getLevelName)
from typing import Mapping

LOG_FMT = """
--  {name}
level:    {levelname}
time:     {asctime}
module:   {module}
line:     {lineno}
function: {funcName}
message:  |-
{message}
"""

DATE_FMT = "%Y-%m-%d %H:%M:%S"
