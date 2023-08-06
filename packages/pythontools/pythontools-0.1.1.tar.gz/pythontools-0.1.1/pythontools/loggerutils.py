"""
Logging related utilities.
"""

import logging
from datetime import datetime

from .ansicolors import color


class ColoredFormatter(logging.Formatter):
    """
    A logging formatter using ansi code to format the message.
    """

    COLORS = {
        'WARNING': 'yellow',
        'INFO': None,
        'DEBUG': 'cyan',
        'CRITICAL': 'red',
        'ERROR': 'red'
    }

    def format(self, record):
        level_name = record.levelname
        level_color = None
        if level_name in ColoredFormatter.COLORS:
            level_color = ColoredFormatter.COLORS[level_name]
        time = datetime.fromtimestamp(record.created).strftime('%H:%M:%S')
        colored_time = color(time, style='bold')
        if record.args:
            colored_msg = color(record.msg % record.args, fg=level_color)
        else:
            colored_msg = color(record.msg, fg=level_color)
        return '%s - %s' % (colored_time, colored_msg)
