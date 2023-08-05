"""
:Author: Almer Mendoza
:Since: 10/10/2018
"""
import logging

_logging_module = None

def _get_color(color=None):
  """Get color name from pre-defined color list"""
  if color is None and not color:
    raise ValueError('Must have color code')

  colors = {
    'PURPLE':'\033[96m',
    'MAGENTA':'\033[95m',
    'BLUE':'\033[94m',
    'GREEN':'\033[92m',
    'YELLOW':'\033[93m',
    'RED':'\033[91m',
    'DARKGRAY':'\033[90m',
    'GREY':'\033[0m',
    'WHITE':'\033[1m'
  }

  if color not in colors:
    raise KeyError('Use a proper color name: {}'.format(list(colors.keys())))

  return colors[color]

def _get_message():
  """Get message parts"""
  return [
    '{}%(asctime)s{}'.format(_get_color('DARKGRAY'), _get_color('GREY')),
    '{}%(name)-12s{}'.format(_get_color('PURPLE'), _get_color('GREY')),
    '%(levelname)-8s',
    '%(message)s'
  ]

def _set_level_format(level=None, color='WHITE'):
  """Set logging format based on level and color"""
  global _logging_module

  FORMAT = '{}{}{}'
  parsed_format = FORMAT.format(
    _get_color(color),
    _logging_module.getLevelName(level),
    _get_color('GREY')
  )

  if _logging_module.DEBUG is not None:
    parsed_level = _logging_module.DEBUG

  if level is not None:
    parsed_level = level

  if parsed_level is not None:
    _logging_module.addLevelName(parsed_level, parsed_format)

  return True

def RainbowLogger(name=None, no_time=False, new_logging=None):
  """A customized logger built on top of Python's logging"""
  global _logging_module

  _logging_module = logging
  if new_logging is not None:
    _logging_module = new_logging

  _set_level_format(_logging_module.DEBUG, 'BLUE')
  _set_level_format(_logging_module.INFO, 'GREEN')
  _set_level_format(_logging_module.WARNING, 'YELLOW')
  _set_level_format(_logging_module.ERROR, 'RED')
  _set_level_format(_logging_module.CRITICAL, 'MAGENTA')

  logger = _logging_module.getLogger(__name__ if name is None else name)
  handler = _logging_module.StreamHandler()
  (time, name, level, message) = _get_message()
  final_message = '{} {} {}\t{}'.format(time, name, level, message)

  if no_time:
    final_message = '{} {}\t{}'.format(name, level, message)

  formatter = _logging_module.Formatter(final_message)

  handler.setFormatter(formatter)
  logger.addHandler(handler)
  logger.setLevel(_logging_module.DEBUG)

  return logger

def __init__():
  return RainbowLogger
