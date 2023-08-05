# Rainbow Bridge Logger

A wrapper for the native logging module of Python.

## Installation

```sh
pip install rainbow-bridge-logger # or pip3
```

## Usage

```python
from rainbow import RainbowLogger

# __name__ will get the current context
# but you can pass any text you want, for identification
logger = RainbowLogger(__name__)

logger.info('my info')
logger.warning('my warn')
logger.error('my error')
logger.debug('my debug')
```

Which should output the following:

![Output for logger](/res/rainbow-logger-output.png)


### Options

#### Unset time in logging

```python
logger = RainbowLogger(no_time=False)
```

#### Custom naming

```python
logger = RainbowLogger('my_logger')
```

## Todo

- [ ] Improve possible arguments to be passed
  - [x] Added no_time argument to remove timestamps
- [ ] Add capability for custom formats and coloring
- [ ] Improve pathing for module
- [ ] Allow easy integration with other frameworks that uses logging
- [x] Publish to pip to be usable anywhere
- [x] Create installation section
- [x] Improve README
- [x] Create usage section

## Note

Tested on both Python 2.7 and Python 3.6

## Author

- Almer T. Mendoza
